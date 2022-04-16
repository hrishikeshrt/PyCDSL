#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Models for Lexicon Access
"""

# TODO: XML Parse per Dictionary

###############################################################################

import logging
from functools import lru_cache
from typing import Dict

from peewee import DatabaseProxy, Model, DecimalField, CharField, TextField

import bs4
from indic_transliteration import sanscript

from .utils import validate_scheme, transliterate_between
from .constants import INTERNAL_SCHEME, DEFAULT_SCHEME

###############################################################################

LOGGER = logging.getLogger(__name__)

###############################################################################


class Lexicon(Model):
    """Lexicon Model"""
    id = DecimalField(unique=True, decimal_places=2, column_name="lnum")
    key = CharField(index=True)
    data = TextField()

    def __str__(self) -> str:
        return f"{self.id}: {self.key}"

    class Meta:
        database = DatabaseProxy()

# --------------------------------------------------------------------------- #


class Entry:
    """
    Lexicon Entry

    Wraps instances of Lexicon model which respresent query results
    """
    def __init__(
        self,
        lexicon_entry: Lexicon,
        lexicon_id: str = None,
        scheme: str = None,
        transliterate_keys: bool = True
    ):
        """
        Lexicon Entry

        Parameters
        ----------
        lexicon_entry : Lexicon
            Instance of Lexicon model
        lexicon_id : str, optional
            ID of the Lexicon to which the entry belongs
        scheme : str, optional
            Output transliteration scheme.
            If valid, parts of the `data` in lexicon which are enclosed in
            `<s>` tags will be transliterated to `scheme`.
            If invalid or None, no transliteration will take place.
            The default is None.
        transliterate_keys : bool, optional
            If True, the keys in lexicon will be transliterated to `scheme`.
            The default is True.
        """
        self._entry = lexicon_entry

        self.id = self._entry.id
        self.key = self._entry.key
        self.data = self._entry.data

        if lexicon_id is None:
            lexicon_id = self.__class__.__name__.split("Entry")[0]

        self.lexicon_id = lexicon_id

        # Validate Scheme
        valid_scheme = validate_scheme(scheme) or INTERNAL_SCHEME

        # Transliterate
        if valid_scheme != INTERNAL_SCHEME:
            if transliterate_keys:
                self.key = sanscript.transliterate(
                    self._entry.key, INTERNAL_SCHEME, valid_scheme
                )
            else:
                self.key = self._entry.key

            self.data = transliterate_between(
                self._entry.data,
                from_scheme=INTERNAL_SCHEME,
                to_scheme=valid_scheme,
                start_pattern=r"<s>",
                end_pattern=r"</s>"
            )

        self._soup = bs4.BeautifulSoup(self.data, "xml")
        self._body = self._soup.find("body")
        self.__post_init__()

    def __post_init__(self):
        """Placeholder to implement a custom post-init hook"""
        pass

    def transliterate(
        self,
        scheme: str = DEFAULT_SCHEME,
        transliterate_keys: bool = True
    ):
        """Transliterate Data

        Part of the `data` in lexicon that is enclosed in `<s>` tags
        will be transliterated to `scheme`.

        Parameters
        ----------
        scheme : str, optional
            Output transliteration scheme.
            If invalid or None, no transliteration will take place.
            The default is `DEFAULT_SCHEME`.
        transliterate_keys : bool, optional
            If True, the keys in lexicon will be transliterated to `scheme`.
            The default is True.

        Returns
        -------
        object
            Returns a new transliterated instance
        """
        return self.__class__(
            self._entry,
            scheme=scheme,
            transliterate_keys=transliterate_keys
        )

    # NOTE: The cache is only on the instance, while the search functions from
    #       shell or cli re-create the Entry objects, so the cache doesn't
    #       actually save much there.
    @lru_cache(maxsize=1)
    def meaning(self) -> str:
        """Extract meaning of the entry"""
        return self._body.get_text().strip()

    def to_dict(self) -> Dict[str, str]:
        """Get a python `dict` representation of the entry"""
        return {
            "lexicon": self.lexicon_id,
            "id": str(self.id),
            "key": self.key,
            "data": self.data,
            "text": self.meaning()
        }

    def parse(self):
        raise NotImplementedError

    def __repr__(self) -> str:
        classname = self.__class__.__qualname__
        return f"<{classname}: {self.id}: {self.key} = {self.meaning()}>"


###############################################################################


def lexicon_constructor(dict_id: str, table_name: str = None) -> Lexicon:
    """Construct a Lexicon Model

    Parameters
    ----------
    dict_id : str
        Dictionary ID
    table_name : str, optional
        Name of the table in SQLite database.
        If None, it will be inferred as dict_id.lower()
        The default is None.

    Returns
    -------
    object
        Constructed class (a subclass of `Lexicon`) for a dictionary
    """
    table_name = table_name or dict_id.lower()
    class_dict = {
        "Meta": type("Meta", (), {"table_name": table_name})
    }
    bases = (Lexicon,)
    return type(f"{dict_id}Lexicon", bases, class_dict)


def entry_constructor(dict_id: str) -> Entry:
    """Construct an Entry Model

    Parameters
    ----------
    dict_id : str
        Dictionary ID

    Returns
    -------
    object
        Constructed class (a subclass of `Entry`) for a dictionary entry
    """
    return type(f"{dict_id}Entry", (Entry,), {})

###############################################################################
# Custom Lexicon and Entry classes


class AP90Lexicon(Lexicon):
    class Meta:
        table_name = "ap90"


class AP90Entry(Entry):
    pass

# --------------------------------------------------------------------------- #


class MWLexicon(Lexicon):
    class Meta:
        table_name = "mw"


class MWEntry(Entry):
    pass

###############################################################################
