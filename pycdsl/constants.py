#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyCDSL Constants
"""

###############################################################################

from pathlib import Path
from indic_transliteration import sanscript

###############################################################################

SERVER_URL = "https://www.sanskrit-lexicon.uni-koeln.de"

###############################################################################

INTERNAL_SCHEME = sanscript.SLP1
DEFAULT_SCHEME = sanscript.DEVANAGARI

###############################################################################

SEARCH_MODE_KEY = "key"
SEARCH_MODE_VALUE = "value"
SEARCH_MODE_BOTH = "both"

SEARCH_MODES = [SEARCH_MODE_KEY, SEARCH_MODE_VALUE, SEARCH_MODE_BOTH]
DEFAULT_SEARCH_MODE = SEARCH_MODE_KEY

###############################################################################

DEFAULT_DICTIONARIES = [
    # Sanskrit-English
    # ----------------
    "MW", "AP90",
    # "WIL", "YAT", "GST", "MW72", "BEN", "LAN", "CAE", "MD", "SHS",

    # English-Sanskrit
    # ----------------
    "MWE", "AE",  # "BOR",

    # Sanskrit-Sanskrit
    # -----------------
    # "VCP", "SKD", "ARMH",

    # Special
    # ---------
    # "INM", "MCI", "VEI" "PUI", "PE", "SNP",
]

ENGLISH_DICTIONARIES = ["MWE", "BOR", "AE"]

###############################################################################

HOME_DIR = Path.home()
DEFAULT_CORPUS_DIR = HOME_DIR / "cdsl_data"

DEFAULT_HISTORY_FILE = HOME_DIR / ".cdsl_history"
DEFAULT_STARTUP_SCRIPT = HOME_DIR / ".cdslrc"

###############################################################################
