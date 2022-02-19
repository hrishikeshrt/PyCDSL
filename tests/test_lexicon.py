#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for `pycdsl.lexicon`"""

import json
import logging

import pytest

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from pycdsl.constants import DEFAULT_SCHEME, INTERNAL_SCHEME
from pycdsl.models import Entry, Lexicon

###############################################################################


def test_initialization(default_dict):
    assert default_dict.input_scheme == INTERNAL_SCHEME
    assert default_dict.output_scheme == INTERNAL_SCHEME


def test_set_scheme(local_dict):
    local_dict.set_scheme(DEFAULT_SCHEME, DEFAULT_SCHEME)
    assert local_dict.input_scheme == DEFAULT_SCHEME
    assert local_dict.output_scheme == DEFAULT_SCHEME


def test_download(download_dict, default_download_path, caplog):
    assert download_dict is not None
    download_zip_path = default_download_path / f"{download_dict.id}.web.zip"
    assert download_zip_path.exists()

    caplog.set_level(logging.INFO)
    status = download_dict.download(default_download_path)
    assert status is True
    assert caplog.record_tuples == [(
        "pycdsl.lexicon",
        logging.INFO,
        f"Data for dictionary '{download_dict.id}' is up-to-date."
    )]


def test_lexicon_setup(
    download_dict,
    default_download_path,
    default_symlink_path
):
    status = download_dict.setup(default_download_path, default_symlink_path)
    assert status is True

    symlink_path = default_symlink_path / f"{download_dict.id}.db"

    assert symlink_path.is_symlink()
    assert download_dict.db == str(symlink_path)


def test_lexicon_connect(local_dict):
    assert issubclass(local_dict._lexicon, Lexicon)
    assert issubclass(local_dict._entry, Entry)

###############################################################################


def test_lexicon_iteration(local_dict):
    for entry in local_dict:
        assert isinstance(entry, Entry)
        break


def test_stats(local_dict):
    assert isinstance(local_dict.stats(), dict)
    assert local_dict.stats()['total'] >= local_dict.stats()['distinct']

###############################################################################


def test_lexicon_getitem(local_dict):
    for entry in local_dict:
        break

    fetched_entry = local_dict[entry.id]

    assert isinstance(fetched_entry, Entry)
    assert fetched_entry.id == entry.id
    assert fetched_entry.key == entry.key
    assert fetched_entry.data == entry.data


def test_lexicon_getitem_error_1(local_dict):
    with pytest.raises(KeyError) as exc_info:
        local_dict['invalid_entry_id']
    assert exc_info.type is KeyError

###############################################################################


def test_lexicon_entry(local_dict):
    for entry in local_dict:
        break

    fetched_entry = local_dict.entry(entry.id)
    assert isinstance(fetched_entry, Entry)
    assert fetched_entry.id == entry.id
    assert fetched_entry.key == entry.key
    assert fetched_entry.data == entry.data


def test_lexicon_entry_error_1(local_dict):
    assert local_dict.entry('invalid_entry_id') is None

###############################################################################


def test_entry_transliteration(local_dict):
    for entry in local_dict:
        break

    key_default = entry.key
    key_iast = transliterate(
        key_default,
        local_dict.output_scheme,
        sanscript.IAST
    )
    key_velthuis = transliterate(
        key_default,
        local_dict.output_scheme,
        sanscript.VELTHUIS
    )
    assert entry.transliterate(scheme=sanscript.IAST).key == key_iast
    assert entry.transliterate(scheme=sanscript.VELTHUIS).key == key_velthuis


def test_dump(local_dict, tmp_path):
    dump_path = tmp_path / "dump.json"
    data = local_dict.dump(dump_path)
    assert dump_path.exists()
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    dumped_data = json.loads(dump_path.read_text())
    assert data == dumped_data
