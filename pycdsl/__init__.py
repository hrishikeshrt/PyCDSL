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
__version__ = '0.2.0'

###############################################################################

from .models import DEFAULT_SCHEME, INTERNAL_SCHEME    # noqa
from .pycdsl import CDSLDict, CDSLCorpus               # noqa
