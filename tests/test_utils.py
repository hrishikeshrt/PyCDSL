#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for `pycdsl.utils`"""

import logging
from pycdsl.utils import validate_scheme, transliterate_between


def test_validate_scheme(caplog):
    assert validate_scheme("devanagari") == "devanagari"
    assert validate_scheme("IAST") == "iast"
    assert validate_scheme("invalid-scheme-1") is None
    assert validate_scheme(None) is None
    assert validate_scheme("invalid-scheme-2") is None

    assert caplog.record_tuples == [
        (
            "pycdsl.utils",
            logging.WARNING,
            "Invalid transliteration scheme 'invalid-scheme-1'."
        ),
        (
            "pycdsl.utils",
            logging.WARNING,
            "Invalid transliteration scheme 'invalid-scheme-2'."
        )
    ]


def test_transliterate_between():
    text = "Lord <s>रामः</s> was a <s>राजा</s> of <s>अयोध्या</s>."
    correct_output = "Lord <s>rāmaḥ</s> was a <s>rājā</s> of <s>ayodhyā</s>."
    output = transliterate_between(text, 'devanagari', 'iast', r"<s>", r"</s>")
    assert output == correct_output
