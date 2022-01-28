#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Models for Lexicon Access
"""

# TODO: XML Parse per Dictionary

###############################################################################

import re
from functools import lru_cache

from peewee import (DatabaseProxy, Model,
                    DecimalField, CharField, TextField)
# from playhouse.shortcuts import model_to_dict

import bs4

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

###############################################################################

INTERNAL_SCHEME = sanscript.SLP1
EXTERNAL_SCHEME = sanscript.DEVANAGARI

###############################################################################


def to_internal(matchobj_or_str):
    if isinstance(matchobj_or_str, str):
        target = matchobj_or_str
        start = ""
        end = ""
    if isinstance(matchobj_or_str, re.Match):
        target = matchobj_or_str.group(1)
        start = r"<s>"
        end = r"</s>"

    replacement = transliterate(target, EXTERNAL_SCHEME, INTERNAL_SCHEME)
    return f"{start}{replacement}{end}"


def to_external(matchobj_or_str):
    if isinstance(matchobj_or_str, str):
        target = matchobj_or_str
        start = ""
        end = ""
    if isinstance(matchobj_or_str, re.Match):
        target = matchobj_or_str.group(1)
        start = r"<s>"
        end = r"</s>"

    replacement = transliterate(target, INTERNAL_SCHEME, EXTERNAL_SCHEME)
    return f"{start}{replacement}{end}"

###############################################################################


class SanskritCharField(CharField):
    def db_value(self, value):
        return to_internal(value)

    def python_value(self, value):
        return to_external(value)


class SanskritXMLField(TextField):
    def db_value(self, value):
        start = r"<s>"
        end = r"</s>"
        pattern = "%s(.*?)%s" % (re.escape(start), re.escape(end))
        return re.sub(pattern, to_internal, value, flags=re.DOTALL)

    def python_value(self, value):
        start = r"<s>"
        end = r"</s>"
        pattern = "%s(.*?)%s" % (re.escape(start), re.escape(end))
        return re.sub(pattern, to_external, value, flags=re.DOTALL)

###############################################################################


class BaseLexicon(Model):
    """Base Lexicon Model without any transliteration"""
    # Default scheme for most dictionaries is SLP1
    id = DecimalField(unique=True, decimal_places=2, db_column='lnum')
    key = CharField(index=True)
    data = TextField()

    def __str__(self):
        return f'{self.id}: {self.key}'

    class Meta:
        database = DatabaseProxy()

# --------------------------------------------------------------------------- #


class PlainKeysLexicon(Model):
    """Lexicon model with non-transliterated keys"""
    id = DecimalField(unique=True, decimal_places=2, db_column='lnum')
    key = CharField(index=True)
    data = SanskritXMLField()

    def __str__(self):
        return f'{self.id}: {self.key}'

    class Meta:
        database = DatabaseProxy()

# --------------------------------------------------------------------------- #


class SanskritLexicon(Model):
    """Lexicon model with transliterated keys and data"""
    id = DecimalField(unique=True, decimal_places=2, db_column='lnum')
    key = SanskritCharField(index=True)
    data = SanskritXMLField()

    def __str__(self):
        return f'{self.id}: {self.key}'

    class Meta:
        database = DatabaseProxy()

# --------------------------------------------------------------------------- #


class Entry:
    """Wrapper for Lexicon Entry"""
    def __init__(self, entry):
        self.id = entry.id
        self.key = entry.key
        self.data = entry.data

        self._entry = entry
        self._soup = bs4.BeautifulSoup(self.data, 'xml')
        self._body = self._soup.find('body')

    @property
    @lru_cache(maxsize=1)
    def meaning(self):
        return self._body.get_text().strip()

    def parse(self):
        raise NotImplementedError

    def __repr__(self):
        classname = self.__class__.__qualname__
        return f'<{classname}: {self.id}: {self.key} = {self.meaning}>'


###############################################################################


def lexicon_constructor(
    dict_id,
    table_name=None,
    transliterate_keys=True,
    transliterate_data=True
):
    """Construct a Lexicon Model

    Parameters
    ----------
    dict_id : str
        Dictionary ID
    table_name : str, optional
        Name of the table in SQLite database.
        If None, it will be inferred as dict_id.lower()
        The default is None.
    transliterate_keys : bool, optional
        If True, the keys in lexicon will be transliterated to Devanagari.
        The default is True.
    transliterate_data : bool, optional
        If True, part of the data in lexicon that is enclosed in <s> tags
        will be transliterated to Devanagari.
        If False, the transliterate_keys option will be assumed to be False.
        The default is True.

    Returns
    -------
    object
        Constructed class for lexicon
    """
    table_name = table_name or dict_id.lower()
    class_dict = {
        "Meta": type("Meta", (), {'table_name': table_name})
    }
    if not transliterate_data:
        bases = (BaseLexicon,)
        model_desc = "Base"
    elif not transliterate_keys:
        bases = (PlainKeysLexicon,)
        model_desc = "PlainKeys"
    else:
        bases = (SanskritLexicon,)
        model_desc = ""
    return type(f"{dict_id}{model_desc}Lexicon", bases, class_dict)


def entry_constructor(dict_id):
    """Construct an Entry Model

    Parameters
    ----------
    dict_id : str
        Dictionary ID

    Returns
    -------
    object
        Constructed class for dictionary entry
    """
    return type(f"{dict_id}Entry", (Entry,), {})

###############################################################################
# Custom Lexicon and Entry classes


class AP90Lexicon(SanskritLexicon):
    class Meta:
        table_name = 'ap90'


class AP90Entry(Entry):
    pass

# --------------------------------------------------------------------------- #


class MWLexicon(SanskritLexicon):
    class Meta:
        table_name = 'mw'


class MWEntry(Entry):
    pass

###############################################################################
