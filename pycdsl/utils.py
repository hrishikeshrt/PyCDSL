#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility Functions
"""

import re

from indic_transliteration.sanscript import SCHEMES, transliterate

###############################################################################


def validate_scheme(scheme):
    """Validate the name of transliteration scheme"""
    return scheme in SCHEMES


def transliterate_between(
    text, from_scheme, to_scheme, start_pattern, end_pattern
):
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
