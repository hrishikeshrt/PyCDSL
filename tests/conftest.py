#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Global Fixtures"""

###############################################################################

import pytest

from pycdsl.constants import SERVER_URL
from pycdsl.lexicon import CDSLDict
from pycdsl.corpus import CDSLCorpus

###############################################################################


@pytest.fixture(scope="session")
def cdsl_homepage():
    """Fixture for CDSL Homepage"""
    import requests
    return requests.get(SERVER_URL)


@pytest.fixture(scope="session")
def default_path(tmp_path_factory):
    return tmp_path_factory.mktemp("cdsl_data")

###############################################################################


@pytest.fixture(scope="session")
def default_dict_options():
    return {
        "id": "WIL",
        "date": "1832",
        "name": "Wilson Sanskrit-English Dictionary",
        "url": f"{SERVER_URL}/scans/WILScan/2020/web/webtc/download.html",
        "input_scheme": None,
        "output_scheme": None,
        "transliterate_keys": True
    }


@pytest.fixture(scope="session")
def default_dict(default_dict_options):
    return CDSLDict(**default_dict_options)


@pytest.fixture(scope="session")
def default_download_path(default_path, default_dict):
    return default_path / "dict" / default_dict.id


@pytest.fixture(scope="session")
def default_symlink_path(default_path):
    return default_path / "db"


@pytest.fixture(scope="session")
def download_dict(default_dict_options, default_download_path):
    default_dict_copy = CDSLDict(**default_dict_options)
    if default_dict_copy.download(default_download_path):
        return default_dict_copy


@pytest.fixture(scope="session")
def local_dict(
    default_dict_options,
    default_download_path,
    default_symlink_path
):
    default_dict_copy = CDSLDict(**default_dict_options)
    if default_dict_copy.setup(default_download_path, default_symlink_path):
        default_dict_copy.connect()
        return default_dict_copy

###############################################################################


@pytest.fixture(scope="session")
def default_corpus_options(default_path):
    return {'data_dir': default_path}


@pytest.fixture(scope="session")
def default_corpus(default_corpus_options):
    return CDSLCorpus(**default_corpus_options)


@pytest.fixture(scope="session")
def available_dicts(default_corpus):
    return default_corpus.get_available_dicts()


@pytest.fixture(scope="session")
def installation_list():
    return ["WIL"]


@pytest.fixture(scope="session")
def ready_corpus(default_corpus_options, installation_list):
    corpus = CDSLCorpus(**default_corpus_options)
    corpus.setup(installation_list)
    return corpus


@pytest.fixture(scope="session")
def installed_dicts(ready_corpus):
    return ready_corpus.get_installed_dicts()


###############################################################################
