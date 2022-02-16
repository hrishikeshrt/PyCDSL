#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for `pycdsl.corpus`"""

import pytest

from pycdsl.lexicon import CDSLDict
from pycdsl.models import Entry

###############################################################################


def test_homepage_content(cdsl_homepage):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(cdsl_homepage.content.decode(), "html.parser")
    header_text = soup.find("div", attrs={"id": "header"}).get_text()
    logo_title = soup.find("img", attrs={"id": "logo"}).attrs["title"]
    assert "Cologne Digital Sanskrit Dictionaries" in header_text
    assert "Cologne Sanskrit Lexicon" in logo_title


def test_available_dicts(available_dicts):
    assert isinstance(available_dicts, dict)
    for dict_id, cdsl_dict in available_dicts.items():
        assert dict_id == cdsl_dict.id
        assert isinstance(cdsl_dict, CDSLDict)


def test_corpus_setup(default_corpus, installation_list):
    assert default_corpus.setup(installation_list) is True


def test_corpus_setup_error_1(default_corpus, installation_list, caplog):
    with pytest.raises(ValueError) as exc_info:
        default_corpus.setup(installation_list[0])
    assert exc_info.type is ValueError


def test_installed_dicts(installed_dicts, installation_list):
    assert isinstance(installed_dicts, dict)
    assert list(installed_dicts) == installation_list


def test_corpus_getattr(ready_corpus, installation_list):
    for installed_dict in installation_list:
        assert hasattr(ready_corpus, installed_dict)
        assert (
            getattr(ready_corpus, installed_dict)
            is ready_corpus.dicts[installed_dict]
        )
    with pytest.raises(AttributeError) as exc_info:
        getattr(ready_corpus, 'invalid_dictionary_id')
    assert exc_info.type is AttributeError


def test_corpus_getitem(ready_corpus, installation_list):
    for installed_dict in installation_list:
        assert (
            ready_corpus[installed_dict]
            is ready_corpus.dicts[installed_dict]
        )
    with pytest.raises(KeyError) as exc_info:
        ready_corpus['invalid_dictionary_id']
    assert exc_info.type is KeyError


def test_corpus_iteration(ready_corpus, installation_list):
    for cdsl_dict in ready_corpus:
        assert isinstance(cdsl_dict, CDSLDict)

    assert set(_dict.id for _dict in ready_corpus) == set(installation_list)


@pytest.mark.parametrize("pattern,limit", [("अ", 1), ("राम", 1)])
def test_search(ready_corpus, installation_list, pattern, limit):
    results = ready_corpus.search(pattern, limit=limit, omit_empty=True)
    for installed_dict in installation_list:
        assert len(results[installed_dict]) <= limit
        first_result = results[installed_dict][0]
        assert isinstance(first_result, Entry)

###############################################################################
