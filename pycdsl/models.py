#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Models for Lexicon Access
"""

# TODO: XML Parse per Dictionary

###############################################################################

import logging
from functools import lru_cache

from peewee import (DatabaseProxy, Model,
                    DecimalField, CharField, TextField)
# from playhouse.shortcuts import model_to_dict

import bs4
from indic_transliteration import sanscript

from .utils import validate_scheme, transliterate_between

###############################################################################

LOGGER = logging.getLogger(__name__)

###############################################################################

INTERNAL_SCHEME = sanscript.SLP1
DEFAULT_SCHEME = sanscript.DEVANAGARI

###############################################################################


class Lexicon(Model):
    """Lexicon Model"""
    id = DecimalField(unique=True, decimal_places=2, db_column='lnum')
    key = CharField(index=True)
    data = TextField()

    def __str__(self):
        return f'{self.id}: {self.key}'

    class Meta:
        database = DatabaseProxy()

# --------------------------------------------------------------------------- #


class Entry:
    """
    Lexicon Entry

    Wraps instances of Lexicon model which respresent query results
    """
    def __init__(self, lexicon_entry, scheme=None, transliterate_keys=True):
        """
        Lexicon Entry

        Parameters
        ----------
        lexicon_entry : Lexicon
            Instance of Lexicon model
        scheme : str, optional
            Output transliteration scheme.
            If valid, parts of the `data` in lexicon which are enclosed in
            `<s>` tags will be transliterated to `scheme`.
            If invalid or None, no transliteration will take place.
            The default is None.
        transliterate_keys : bool, optional
            If True, the keys in lexicon will be transliterated to `scheme`.
            The default is True.
        """
        self._entry = lexicon_entry

        self.id = self._entry.id
        self.key = self._entry.key
        self.data = self._entry.data

        # Validate Scheme
        if scheme is None:
            scheme = INTERNAL_SCHEME

        scheme_is_valid = validate_scheme(scheme)
        if not scheme_is_valid:
            LOGGER.warning(f"Invalid transliteration scheme '{scheme}'.")

        # Transliterate
        if scheme_is_valid and scheme != INTERNAL_SCHEME:
            if transliterate_keys:
                self.key = sanscript.transliterate(
                    self._entry.key, INTERNAL_SCHEME, scheme
                )
            else:
                self.key = self._entry.key

            self.data = transliterate_between(
                self._entry.data,
                from_scheme=INTERNAL_SCHEME,
                to_scheme=scheme,
                start_pattern=r"<s>",
                end_pattern=r"</s>"
            )

        self._soup = bs4.BeautifulSoup(self.data, 'xml')
        self._body = self._soup.find('body')

    def transliterate(self, scheme=DEFAULT_SCHEME, transliterate_keys=True):
        """Transliterate Data

        Part of the `data` in lexicon that is enclosed in `<s>` tags
        will be transliterated to `scheme`.

        Parameters
        ----------
        scheme : str, optional
            Output transliteration scheme.
            If invalid or None, no transliteration will take place.
            The default is `DEFAULT_SCHEME`.
        transliterate_keys : bool, optional
            If True, the keys in lexicon will be transliterated to `scheme`.
            The default is True.

        Returns
        -------
        object
            Returns a new transliterated instance
        """
        return self.__class__(
            self._entry,
            scheme=scheme,
            transliterate_keys=transliterate_keys
        )

    @lru_cache(maxsize=1)
    def meaning(self):
        return self._body.get_text().strip()

    def parse(self):
        raise NotImplementedError

    def __repr__(self):
        classname = self.__class__.__qualname__
        return f'<{classname}: {self.id}: {self.key} = {self.meaning()}>'


###############################################################################


def lexicon_constructor(dict_id, table_name=None):
    """Construct a Lexicon Model

    Parameters
    ----------
    dict_id : str
        Dictionary ID
    table_name : str, optional
        Name of the table in SQLite database.
        If None, it will be inferred as dict_id.lower()
        The default is None.

    Returns
    -------
    object
        Constructed class for lexicon
    """
    table_name = table_name or dict_id.lower()
    class_dict = {
        "Meta": type("Meta", (), {'table_name': table_name})
    }
    bases = (Lexicon,)
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


class AP90Lexicon(Lexicon):
    class Meta:
        table_name = 'ap90'


class AP90Entry(Entry):
    pass

# --------------------------------------------------------------------------- #


class MWLexicon(Lexicon):
    class Meta:
        table_name = 'mw'


class MWEntry(Entry):
    pass

###############################################################################
