#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for `pycdsl.utils`"""

import pytest
from pycdsl.utils import validate_scheme, transliterate_between


@pytest.mark.parametrize("input_scheme,result,log_messages", [
    ("devanagari", "devanagari", []),
    ("IAST", "iast", []),
    ("Velthuis", "velthuis", []),
    ("invalid-1", None, ["Invalid transliteration scheme 'invalid-1'."]),
    ("invalid-2", None, ["Invalid transliteration scheme 'invalid-2'."]),
    (None, None, [])
])
def test_validate_scheme(caplog, input_scheme, result, log_messages):
    assert validate_scheme(input_scheme) == result
    assert caplog.messages == log_messages


@pytest.mark.parametrize("text,_from,_to,_start,_end,result", [
    ("Lord <s>रामः</s> was a <s>राजा</s> of <s>अयोध्या</s> इति श्रूयते",
     "devanagari", "iast", r"<s>", r"</s>",
     "Lord <s>rāmaḥ</s> was a <s>rājā</s> of <s>ayodhyā</s> इति श्रूयते"),
    ("Lord <s>रामः</s> of <s>अयोध्या</s>.",
     "devanagari", "devanagari", r"<s>", r"</s>",
     "Lord <s>रामः</s> of <s>अयोध्या</s>."),
])
def test_transliterate_between(text, _from, _to, _start, _end, result):
    assert result == transliterate_between(text, _from, _to, _start, _end)
