#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyCDSL

Python Interface to Cologne Digital Sanskrit Lexicon (CDSL).
"""
# Created on Sat Apr 17 18:47:35 2021

###############################################################################

__author__ = "Hrishikesh Terdalkar"
__email__ = 'hrishikeshrt@linuxmail.org'
__version__ = '0.4.0'

###############################################################################

from .corpus import CDSLCorpus               # noqa
from .lexicon import CDSLDict                # noqa
from .shell import CDSLShell                 # noqa
from .constants import (                     # noqa
    SERVER_URL,
    DEFAULT_SCHEME, INTERNAL_SCHEME,
    DEFAULT_CORPUS_DIR,
    DEFAULT_DICTIONARIES, ENGLISH_DICTIONARIES
)
