#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility Functions
"""

import re
import logging

from indic_transliteration.sanscript import SCHEMES, transliterate
from .constants import SEARCH_MODES

###############################################################################

LOGGER = logging.getLogger(__name__)

###############################################################################


def validate_search_mode(mode: str) -> str or None:
    """Validate the search mode

    Parameters
    ----------
    mode : str
        Search mode

    Returns
    -------
    str or None
        If mode is valid, mode.lower()
        otherwise, None.
    """
    if mode is not None:
        _mode = mode.lower() if mode.lower() in SEARCH_MODES else None
        if _mode is None:
            LOGGER.warning(f"Invalid search mode '{mode}'.")
    else:
        _mode = None

    return _mode


def validate_scheme(scheme: str) -> str or None:
    """Validate the name of transliteration scheme

    Parameters
    ----------
    scheme : str
        Name of the transltieration scheme

    Returns
    -------
    str or None
        If scheme is valid, scheme.lower()
        otherwise, None.
    """
    if scheme is not None:
        _scheme = scheme.lower() if scheme.lower() in SCHEMES else None
        if _scheme is None:
            LOGGER.warning(f"Invalid transliteration scheme '{scheme}'.")
    else:
        _scheme = None

    return _scheme


def transliterate_between(
    text: str,
    from_scheme: str,
    to_scheme: str,
    start_pattern: str,
    end_pattern: str
) -> str:
    """Transliterate the text appearing between two patterns

    Only the text appearing between patterns `start_pattern` and `end_pattern`
    it transliterated.
    `start_pattern` and `end_pattern` can appear multiple times in the full
    text, and for every occurrence, the text between them is transliterated.

    `from_scheme` and `to_scheme` should be compatible with scheme names from
    `indic-transliteration`

    Parameters
    ----------
    text : str
        Full text
    from_scheme : str
        Input transliteration scheme
    to_scheme : str
        Output transliteration scheme
    start_pattern : regexp
        Pattern describing the start tag
    end_pattern : regexp
        Pattern describing the end tag
    """

    if from_scheme == to_scheme:
        return text

    def transliterate_match(matchobj):
        target = matchobj.group(1)
        replacement = transliterate(target, from_scheme, to_scheme)
        return f"{start_pattern}{replacement}{end_pattern}"

    pattern = "%s(.*?)%s" % (re.escape(start_pattern), re.escape(end_pattern))
    return re.sub(pattern, transliterate_match, text, flags=re.DOTALL)


###############################################################################
