#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CDSL Corpus Management

Download dictionaries from https://www.sanskrit-lexicon.uni-koeln.de/
"""

###############################################################################

from pathlib import Path
from dataclasses import dataclass, field
from functools import cached_property, lru_cache
import zipfile

from peewee import fn
from playhouse.db_url import connect

import bs4
import requests
from requests_downloader import downloader

from .models import (
    MWLexicon, MWEntry,
    AP90Lexicon, AP90Entry,
    lexicon_constructor, entry_constructor
)

###############################################################################

SERVER_URL = "https://www.sanskrit-lexicon.uni-koeln.de"

###############################################################################


DICTIONARIES = {
    "MW": (MWLexicon, MWEntry),
    "AP90": (AP90Lexicon, AP90Entry),
}

ENGLISH_DICTIONARIES = ["MWE", "BOR", "AE"]

###############################################################################

HOME_DIR = Path.home()
COLOGNE_DIR = HOME_DIR / "cdsl_data"

###############################################################################


@dataclass(eq=False)
class CDSLDict:
    """Dictionary from CDSL"""
    id: str
    date: str
    name: str
    url: str = field(repr=False)
    db: str = field(repr=False, default=None)
    english_keys: bool = field(repr=False, default=False)

    # ----------------------------------------------------------------------- #

    def download(self, download_dir, symlink_dir=None):
        """Download and extract dictionary data

        Parameters
        ----------
        download_dir : str or Path
            Full path of directory where the dictionary data should be
            downloaded and extracted
        symlink_dir : str or Path, optional
            Full path of the directory where the symbolink links to the
            SQLite database of dictionary will be created
            If None, symbolic links aren't created.
            The default is None.

        Returns
        -------
        bool
            True if successfully downloaded or already up-to-date
        """
        up_to_date = False

        html = requests.get(self.url).content.decode()
        soup = bs4.BeautifulSoup(html, "html.parser")
        footer = soup.find("div", attrs={"id": "footer"})
        last_modified = footer.find("p").get_text().split(":", 1)[-1].strip()

        download_dir = Path(download_dir)

        last_modified_file = download_dir / "last_modified.txt"
        database_filename = f"{self.id.lower()}.sqlite"
        database_path = download_dir / "web" / "sqlite" / database_filename
        self.db = str(database_path)

        download_dir.mkdir(parents=True, exist_ok=True)

        if last_modified_file.exists():
            local_last_modified = last_modified_file.read_text().strip()
            up_to_date = (local_last_modified == last_modified)

        if not up_to_date:
            # not up-to-date
            # backup current file
            download_path = download_dir / f"{self.id}.web.zip"
            backup_path = download_dir / f"{self.id}.web.zip.bak"
            if download_path.exists():
                backup_path = download_path.rename(backup_path)

            # find download link
            lis = soup.find_all("li")
            for li in lis:
                if "Directory 'web' containing displays" in li.get_text():
                    break
            else:
                print("No download link for 'web' displays was found.")
                return False

            web_url = li.find("a")["href"]
            web_url = requests.compat.urljoin(self.url, web_url)

            # download
            success = downloader.download(web_url, download_path=download_path)

            if not success:
                # download failed - restore backup
                print("Something went wrong.")
                if backup_path.exists():
                    print("Restoring ..")
                    backup_path.rename(download_path)
                return False

            # download was sucessful - remove backup
            if backup_path.exists():
                backup_path.unlink()

            # update last modified info
            last_modified_file.write_text(last_modified)

            # extract
            with zipfile.ZipFile(download_path, "r") as zipref:
                zipref.extractall(download_dir)
        else:
            print(f"Dictionary data for '{self.id}' is already up-to-date.")

        # create symlink
        if symlink_dir is not None:
            symlink_dir = Path(symlink_dir)
            symlink_dir.mkdir(parents=True, exist_ok=True)
            symlink_path = symlink_dir / f"{self.id}.db"
            if not symlink_path.exists():
                symlink_path.symlink_to(database_path)
            self.db = str(symlink_path)

        return True

    # ----------------------------------------------------------------------- #

    def connect(self, lexicon_model=None, entry_model=None):
        if lexicon_model is not None and entry_model is not None:
            self._lexicon = lexicon_model
            self._entry = entry_model
        else:
            if self.id in DICTIONARIES:
                self._lexicon, self._entry = DICTIONARIES[self.id]
            else:
                self._lexicon = lexicon_constructor(
                    self.id,
                    english_keys=self.english_keys
                )
                self._entry = entry_constructor(self.id)

        db_url = f"sqlite:///{self.db}"
        self._lexicon.bind(connect(db_url))

    # ----------------------------------------------------------------------- #

    @cached_property
    def stats(self):
        lex = self._lexicon
        total_count = lex.select().count()
        distinct_query = (
            lex
            .select(
                lex.id, lex.key, lex.data, fn.COUNT(lex.key).alias("count")
            )
            .group_by(lex.key)
            .order_by(fn.COUNT(lex.key).desc())
        )
        top = [(item.key, item.count) for item in distinct_query.limit(10)]
        distinct_count = distinct_query.count()
        return {
            "total": total_count,
            "distinct": distinct_count,
            "top": top
        }

    # ----------------------------------------------------------------------- #

    @lru_cache(maxsize=4096)
    def search(self, search_key, ignore_case=False):
        query = self._lexicon.select().where(self._lexicon.key % search_key)
        iquery = self._lexicon.select().where(self._lexicon.key ** search_key)
        search_query = iquery if ignore_case else query
        return [
            self._entry(result)
            for result in search_query
        ]

###############################################################################


@dataclass
class CDSLCorpus:
    """CDSL Corpus"""
    data_dir: str = field(default=None)

    # ----------------------------------------------------------------------- #

    def __post_init__(self):
        self.data_dir = (
            Path(COLOGNE_DIR)
            if self.data_dir is None
            else Path(self.data_dir)
        )
        self.dict_dir = self.data_dir / "dict"
        self.db_dir = self.data_dir / "db"
        self._dicts = {}

    def __getattr__(self, attr: str):
        if attr in self._dicts:
            return self._dicts[attr]
        else:
            raise AttributeError

    # ----------------------------------------------------------------------- #

    def setup(self, dict_ids: list = None):
        """Download and setup CDSL dictionaries in bulk"""
        self.available_dicts = self.get_available_dicts()
        if dict_ids is None:
            download_dicts = self.available_dicts
        elif isinstance(dict_ids, list):
            download_dicts = {
                dict_id: cdsl_dict
                for dict_id, cdsl_dict in self.available_dicts.items()
                if dict_id in dict_ids
            }
        else:
            raise ValueError("`dict_ids` must be a `list` or `None`")

        status = []
        for dict_id, cdsl_dict in download_dicts.items():
            dict_dir = self.dict_dir / dict_id
            success = cdsl_dict.download(
                download_dir=dict_dir,
                symlink_dir=self.db_dir
            )
            status.append(success)
            if success:
                cdsl_dict.connect()
                self._dicts[dict_id] = cdsl_dict

        return bool(status) and all(status)

    def get_available_dicts(self):
        """Fetch a list of dictionaries available for download from CDSL"""
        html = requests.get(SERVER_URL).content.decode()
        soup = bs4.BeautifulSoup(html, "html.parser")
        dl_tags = soup.find_all("a", attrs={"title": "Downloads"})
        dictionaries = {}
        for dl_tag in dl_tags:
            row = dl_tag.find_parent("tr")
            cells = row.find_all("td")
            assert(len(cells) == 4)
            dict_id = cells[0].get_text(" ").strip().split()[0]
            dict_date = cells[1].get_text(" ").strip().split()[0]
            dict_name = cells[2].find("a").get_text(" ").strip()
            dict_download = f"{SERVER_URL}{dl_tag['href']}"
            dict_english_keys = dict_id in ENGLISH_DICTIONARIES

            dictionaries[dict_id] = CDSLDict(
                id=dict_id,
                date=dict_date,
                name=dict_name,
                url=dict_download,
                english_keys=dict_english_keys
            )
        return dictionaries


###############################################################################
