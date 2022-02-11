#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REPL Shell for PyCDSL"""

###############################################################################

import os
import cmd
import logging

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from .corpus import CDSLCorpus
from .utils import validate_scheme
from .constants import INTERNAL_SCHEME, DEFAULT_SCHEME
from . import __version__

###############################################################################


class BasicShell(cmd.Cmd):
    def emptyline(self):
        pass

    def do_shell(self, commad):
        """Execute shell commands"""
        os.system(commad)

    def do_exit(self, arg):
        """Exit the shell"""
        print("Bye")
        return True

    # do_EOF corresponds to Ctrl + D
    do_EOF = do_exit

###############################################################################


class CDSLShell(BasicShell):
    """REPL Interface to CDSL"""

    intro = "Cologne Sanskrit Digital Lexicon (CDSL)\n" \
            "---------------------------------------"
    desc = "Install or load dictionaries by typing `use [DICT_IDS..]` " \
           "e.g. `use MW`.\n" \
           "Type any keyword to search in the selected dictionaries. " \
           "(help or ? for list of options)"
    prompt = "(CDSL::None) "

    def __init__(
        self,
        data_dir=None,
        dict_ids=None,
        input_scheme=None,
        output_scheme=None
    ):
        """REPL Interface to CDSL

        Create an instance of CDSLCorpus as per the providd parameters.
        CDSLCorpus.setup() is called after the command-loop starts.

        Parameters
        ----------
        data_dir : str or None, optional
            Load a CDSL installation instance at the location `data_dir`.
            Passed to CDSLCorpus instance as a keyword argument `data_dir`.
        dict_ids : list or None, optional
            List of dictionary IDs to setup.
            Passed to a CDSLCorpus.setup() as a keyword argument `dict_ids`.
        input_scheme : str or None, optional
            Transliteration scheme for input.
            If None, `DEFAULT_SCHEME` is used.
            The default is None.
        output_scheme : str or None, optional
            Transliteration scheme for output.
            If None, `DEFAULT_SCHEME` is used.
            The default is None.
        """
        super(self.__class__, self).__init__()
        self.debug = False
        self.schemes = [
            sanscript.DEVANAGARI,
            sanscript.IAST,
            sanscript.ITRANS,
            sanscript.VELTHUIS,
            sanscript.HK,
            sanscript.SLP1,
            sanscript.WX,
        ]

        self.input_scheme = validate_scheme(input_scheme) or DEFAULT_SCHEME
        self.output_scheme = validate_scheme(output_scheme) or DEFAULT_SCHEME

        self.cdsl = CDSLCorpus(
            data_dir=data_dir,
            input_scheme=None,
            output_scheme=None
        )
        self.dict_ids = dict_ids
        self.active_dicts = None

        # Search parameters
        self.limit = 50
        self.offset = None

        # Logging
        self.logger = logging.getLogger()  # root logger
        if not self.logger.hasHandlers():
            self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)

    # ----------------------------------------------------------------------- #
    # Debug Mode

    def do_debug(self, arg):
        """Turn debug mode on/off"""
        if arg.lower() in ["true", "on", "yes"]:
            self.debug = True
            self.logger.setLevel(logging.DEBUG)
        if arg.lower() in ["false", "off", "no"]:
            self.debug = False
            self.logger.setLevel(logging.INFO)
        print(f"Debug: {self.debug}")

    # ----------------------------------------------------------------------- #
    # Input/Output Transliteration Scheme

    def complete_input_scheme(self, text, line, begidx, endidx):
        return [sch for sch in self.schemes if sch.startswith(text)]

    def complete_output_scheme(self, text, line, begidx, endidx):
        return [sch for sch in self.schemes if sch.startswith(text)]

    def do_input_scheme(self, scheme):
        """Change the input transliteration scheme"""
        if not scheme:
            print(f"Input scheme: {self.input_scheme}")
        else:
            if scheme not in self.schemes:
                print(f"Invalid scheme. (valid schemes are {self.schemes}")
            else:
                self.input_scheme = scheme
                print(f"Input scheme: {self.input_scheme}")

    def do_output_scheme(self, scheme):
        """Change the output transliteration scheme"""
        if not scheme:
            print(f"Input scheme: {self.output_scheme}")
        else:
            if scheme not in self.schemes:
                print(f"Invalid scheme. (valid schemes are {self.schemes}")
            else:
                self.output_scheme = scheme
                print(f"Output scheme: {self.output_scheme}")

    # ----------------------------------------------------------------------- #
    # Dictionary Information

    def do_info(self, text=None):
        """Display information about active dictionaries"""
        if self.active_dicts is None:
            self.logger.error("Please select a dictionary first.")
        else:
            print(f"Total {len(self.active_dicts)} dictionaries are active.")
            for active_dict in self.active_dicts:
                print(active_dict)

    # ----------------------------------------------------------------------- #

    def do_dicts(self, text=None):
        """Display a list of dictionaries available locally"""
        for _, cdsl_dict in self.cdsl.dicts.items():
            print(cdsl_dict)

    def do_available(self, text=None):
        """Display a list of dictionaries available in CDSL"""
        for _, cdsl_dict in self.cdsl.available_dicts.items():
            print(cdsl_dict)

    # ----------------------------------------------------------------------- #

    def do_update(self, text):
        """Update loaded dictionaries"""
        self.cdsl.setup(list(self.cdsl.dicts), update=True)

    # ----------------------------------------------------------------------- #

    def complete_use(self, text, line, begidx, endidx):
        last_word = text.upper().rsplit(maxsplit=1)[-1] if text else ""
        return [
            dict_id
            for dict_id in self.cdsl.available_dicts
            if dict_id.startswith(last_word)
        ]

    def do_use(self, line):
        """
        Load the specified dictionaries from CDSL.
        If not available locally, they will be installed first.
        """
        dict_ids = line.upper().split()

        self.active_dicts = []
        for dict_id in dict_ids:
            status = (dict_id in self.cdsl.dicts) or self.cdsl.setup([dict_id])
            if status:
                self.active_dicts.append(self.cdsl.dicts[dict_id])
            else:
                self.logger.error(f"Couldn't setup dictionary '{dict_id}'.")

        active_count = len(self.active_dicts)
        active_ids = [active_dict.id for active_dict in self.active_dicts]

        print(f"Using {active_count} dictionaries: {active_ids}")

        if active_count <= 3:
            active_prompt = ",".join(active_ids)
        else:
            active_prompt = f"{active_ids[0]}+{active_count - 1}"
        self.prompt = f"(CDSL::{active_prompt}) "

    # ----------------------------------------------------------------------- #

    def do_show(self, entry_id):
        """Show a specific entry by ID"""
        if self.active_dicts is None:
            self.logger.error("Please select a dictionary first.")
        else:
            for active_dict in self.active_dicts:
                try:
                    result = active_dict.entry(entry_id)
                    print(
                        result.transliterate(
                            scheme=self.output_scheme,
                            transliterate_keys=active_dict.transliterate_keys
                        )
                    )
                    self.logger.debug(f"Data: {result.data}")
                except Exception:
                    result = None

                if result is None:
                    self.logger.warning(
                        f"Entry {entry_id} not found in '{active_dict.id}'."
                    )

    # ----------------------------------------------------------------------- #

    def do_limit(self, text):
        """Limit the number of search results per dictionary"""
        if text:
            try:
                self.limit = int(text.strip())
                if self.limit < 1:
                    self.limit = None
            except Exception:
                self.logger.error("Limit must be an integer.")

        print(f"Limit: {self.limit}")

    # ----------------------------------------------------------------------- #

    def do_version(self, text):
        """Show the current version of PyCDSL"""
        print(f"PyCDSL v{__version__}")

    # ----------------------------------------------------------------------- #

    def default(self, line):
        if self.active_dicts is None:
            self.logger.error("Please select a dictionary first.")
        else:
            for active_dict in self.active_dicts:
                search_pattern = transliterate(
                    line, self.input_scheme, INTERNAL_SCHEME
                ) if active_dict.transliterate_keys else line
                results = active_dict.search(search_pattern, limit=self.limit)
                if not results:
                    continue

                print(f"\nFound {len(results)} results in {active_dict.id}.\n")

                for result in results:
                    print(
                        result.transliterate(
                            scheme=self.output_scheme,
                            transliterate_keys=active_dict.transliterate_keys
                        )
                    )

    def cmdloop(self, intro=None):
        print(self.intro)
        print(self.desc)
        self.cdsl.setup(dict_ids=self.dict_ids)

        print(f"Loaded {len(self.cdsl.dicts)} dictionaries.")

        if self.dict_ids is not None:
            self.do_use(" ".join(self.dict_ids))

        while True:
            try:
                super(self.__class__, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")


###############################################################################
