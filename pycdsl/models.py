#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Models for Lexicon Access
"""

# TODO: XML Parse per Dictionary

###############################################################################

import re
from functools import cached_property

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


def to_internal(matchobj_or_str, /):
    if isinstance(matchobj_or_str, str):
        target = matchobj_or_str
    if isinstance(matchobj_or_str, re.Match):
        target = matchobj_or_str.group()

    return transliterate(target, EXTERNAL_SCHEME, INTERNAL_SCHEME)


def to_external(matchobj_or_str, /):
    if isinstance(matchobj_or_str, str):
        target = matchobj_or_str
    if isinstance(matchobj_or_str, re.Match):
        target = matchobj_or_str.group()

    return transliterate(target, INTERNAL_SCHEME, EXTERNAL_SCHEME)


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


class Lexicon(Model):
    """Basic Lexicon Model"""
    id = DecimalField(unique=True, decimal_places=2, db_column='lnum')
    key = CharField(index=True)
    data = TextField()

    def __str__(self):
        return f'{self.id}: {self.key}'

    class Meta:
        database = DatabaseProxy()

# --------------------------------------------------------------------------- #


class EnglishLexicon(Model):
    """Lexicon Model with English Keys"""
    id = DecimalField(unique=True, decimal_places=2, db_column='lnum')
    key = CharField(index=True)
    data = SanskritXMLField()

    def __str__(self):
        return f'{self.id}: {self.key}'

    class Meta:
        database = DatabaseProxy()

# --------------------------------------------------------------------------- #


class SanskritLexicon(Model):
    """Lexicon Model with Sanskrit Keys"""
    id = DecimalField(unique=True, decimal_places=2, db_column='lnum')
    key = SanskritCharField(index=True)
    data = SanskritXMLField()

    def __str__(self):
        return f'{self.id}: {self.key}'

    class Meta:
        database = DatabaseProxy()

# --------------------------------------------------------------------------- #


class Entry:
    """Wrapper for Entry Model"""
    def __init__(self, entry):
        self.id = entry.id
        self.key = entry.key
        self.data = entry.data

        self._entry = entry
        self._soup = bs4.BeautifulSoup(self.data, 'xml')
        self._body = self._soup.find('body')

    @cached_property
    def meaning(self):
        return self._body.get_text().strip()

    def parse(self):
        raise NotImplementedError

    def __repr__(self):
        classname = self.__class__.__qualname__
        return f'<{classname}: {self.id}: {self.key} = {self.meaning}>'


###############################################################################


def lexicon_constructor(dict_id, table_name=None, english_keys=False):
    """Construct a Lexicon Model

    Parameters
    ----------
    dict_id : str
        Dictionary ID
    table_name : str, optional
        Name of the table in SQLite database.
        If None, it will be inferred as dict_id.lower()
        The default is None.
    english_keys : bool, optional
        True if the lexicon has English keys instead of Sanskrit
        The default is False.

    Returns
    -------
    object
        Constructed class for lexicon
    """
    table_name = table_name or dict_id.lower()
    class_dict = {
        "Meta": type("Meta", (), {'table_name': table_name})
    }
    bases = (EnglishLexicon,) if english_keys else (SanskritLexicon,)
    return type(f"{dict_id}Lexicon", bases, class_dict)


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
