#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REPL Shell for PyCDSL"""

###############################################################################

# import logging
from typing import List

import cmd2
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from .corpus import CDSLCorpus
from .utils import validate_scheme, validate_search_mode
from .constants import (
    INTERNAL_SCHEME,
    DEFAULT_SCHEME,
    SEARCH_MODES,
    DEFAULT_SEARCH_MODE
)
from . import __version__

###############################################################################


class BasicShell(cmd2.Cmd):
    delattr(cmd2.Cmd, "do_edit")
    delattr(cmd2.Cmd, "do_run_pyscript")


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

    schemes = [
        sanscript.DEVANAGARI,
        sanscript.IAST,
        sanscript.ITRANS,
        sanscript.VELTHUIS,
        sanscript.HK,
        sanscript.SLP1,
        sanscript.WX,
    ]
    search_modes = SEARCH_MODES

    def __init__(
        self,
        data_dir: str = None,
        dict_ids: List[str] = None,
        search_mode: str = None,
        input_scheme: str = None,
        output_scheme: str = None,
        history_file: str = None,
        startup_script: str = None
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
        search_mode : str or None, optional
            Search mode to query by `key`, `value` or `both`.
            The default is None.
        input_scheme : str or None, optional
            Transliteration scheme for input.
            If None, `DEFAULT_SCHEME` is used.
            The default is None.
        output_scheme : str or None, optional
            Transliteration scheme for output.
            If None, `DEFAULT_SCHEME` is used.
            The default is None.
        history_file : str or None, optional
            Path to the history file to keep a persistant history.
            If None, the history does not persist across sessions.
            The default is None.
        startup_script : str or None, optional
            Path to the startup script with a list of startup commands
            to be executed after initialization.
            If None, no startup commands are run.
            The default is None.
        """
        super(self.__class__, self).__init__(
            persistent_history_file=history_file,
            startup_script=startup_script,
            allow_cli_args=False
        )
        self.default_category = "Utility Commands"
        remove_settables = [
            "always_show_hint",
            "echo",
            "editor",
            "feedback_to_output",
            "max_completion_items",
        ]
        for settable in remove_settables:
            self.remove_settable(settable)

        # ------------------------------------------------------------------- #
        # Settings

        # Search Mode
        self.search_mode = (
            validate_search_mode(search_mode) or DEFAULT_SEARCH_MODE
        )

        # Transliteration Schemes
        self.input_scheme = validate_scheme(input_scheme) or DEFAULT_SCHEME
        self.output_scheme = validate_scheme(output_scheme) or DEFAULT_SCHEME

        # Search parameters
        self.limit = 50
        self.offset = None

        self.add_settable(
            cmd2.utils.Settable(
                "search_mode",
                str,
                "Search mode",
                self,
                choices=self.search_modes
            )
        )
        self.add_settable(
            cmd2.utils.Settable(
                "input_scheme",
                str,
                "Input transliteration scheme",
                self,
                choices=self.schemes
            )
        )
        self.add_settable(
            cmd2.utils.Settable(
                "output_scheme",
                str,
                "Output transliteration scheme",
                self,
                choices=self.schemes
            )
        )
        self.add_settable(
            cmd2.utils.Settable(
                "limit",
                int,
                "Limit search results",
                self,
                onchange_cb=self._limit_handler
            )
        )

        # ------------------------------------------------------------------- #

        # Corpus Initialisation
        self.cdsl = CDSLCorpus(
            data_dir=data_dir,
            search_mode=None,
            input_scheme=None,
            output_scheme=None
        )
        self.dict_ids = dict_ids
        self.active_dicts = None

        # # Logging
        # self.logger = logging.getLogger()  # root logger
        # if not self.logger.hasHandlers():
        #     self.logger.addHandler(logging.StreamHandler())
        # self.logger.setLevel(logging.INFO)

    # ----------------------------------------------------------------------- #
    # Debug Mode

    # def do_debug(self, arg: str):
    #     """Turn debug mode on/off"""
    #     arg = arg.lower()
    #     if arg in ["true", "on", "yes"]:
    #         self.debug = True
    #         self.logger.setLevel(logging.DEBUG)
    #     if arg in ["false", "off", "no"]:
    #         self.debug = False
    #         self.logger.setLevel(logging.INFO)
    #     print(f"Debug: {self.debug}")

    # ----------------------------------------------------------------------- #

    def _limit_handler(self, name, old_value, new_value):
        if new_value < 0:
            self.limit = None

    # ----------------------------------------------------------------------- #
    # Dictionary Information

    @cmd2.with_category("CDSL Core Commands")
    def do_info(self, _: cmd2.Statement):
        """Display information about active dictionaries"""
        if self.active_dicts is None:
            self.perror("Please select a dictionary first.")
        else:
            self.poutput(
                f"Total {len(self.active_dicts)} dictionaries are active."
            )
            for active_dict in self.active_dicts:
                self.poutput(active_dict)

    @cmd2.with_category("CDSL Core Commands")
    def do_stats(self, _: cmd2.Statement):
        """Display statistics about active dictionaries"""
        if self.active_dicts is None:
            self.perror("Please select a dictionary first.")
        else:
            self.poutput(
                f"Total {len(self.active_dicts)} dictionaries are active."
            )
            for active_dict in self.active_dicts:
                self.poutput("---")
                self.poutput(active_dict)
                self.poutput(
                    active_dict.stats(output_scheme=self.output_scheme)
                )

    # ----------------------------------------------------------------------- #

    @cmd2.with_category("CDSL Core Commands")
    def do_dicts(self, _: cmd2.Statement):
        """Display a list of dictionaries available locally"""
        for _, cdsl_dict in self.cdsl.dicts.items():
            self.poutput(cdsl_dict)

    @cmd2.with_category("CDSL Core Commands")
    def do_available(self, _: cmd2.Statement):
        """Display a list of dictionaries available in CDSL"""
        for _, cdsl_dict in self.cdsl.available_dicts.items():
            self.poutput(cdsl_dict)

    # ----------------------------------------------------------------------- #

    @cmd2.with_category("CDSL Core Commands")
    def do_update(self, _: cmd2.Statement):
        """Update loaded dictionaries"""
        self.cdsl.setup(list(self.cdsl.dicts), update=True)

    # ----------------------------------------------------------------------- #

    def complete_use(self, text, line, begidx, endidx):
        return [
            dict_id
            for dict_id in self.cdsl.available_dicts
            if dict_id.startswith(text.upper())
        ]

    @cmd2.with_category("CDSL Core Commands")
    def do_use(self, line: cmd2.Statement):
        """
        Load the specified dictionaries from CDSL.
        If not available locally, they will be installed first.

        * `all` to load all
        * `none` to unload all
        """
        line = line.upper().strip()
        if not line:
            self.perror("Please provide dictionary ID(s) to use.")
            return
        if line == "NONE":
            self.active_dicts = []
        elif line == "ALL":
            status = self.cdsl.setup()
            if status:
                self.active_dicts = self.cdsl.dicts.values()
            else:
                self.perror("Couldn't setup some dictionary.")
        else:
            dict_ids = line.split()
            self.active_dicts = []
            for dict_id in dict_ids:
                status = (
                    dict_id in self.cdsl.dicts
                ) or self.cdsl.setup([dict_id])
                if status:
                    self.active_dicts.append(self.cdsl.dicts[dict_id])
                else:
                    self.perror(
                        f"Couldn't setup dictionary '{dict_id}'."
                    )

        active_count = len(self.active_dicts)
        active_ids = [active_dict.id for active_dict in self.active_dicts]

        self.poutput(f"Using {active_count} dictionaries: {active_ids}")

        if active_count == 0:
            active_prompt = "None"
        elif active_count <= 3:
            active_prompt = ",".join(active_ids)
        else:
            active_prompt = f"{active_ids[0]}+{active_count - 1}"
        self.prompt = f"(CDSL::{active_prompt}) "

    # ----------------------------------------------------------------------- #

    @cmd2.with_category("CDSL Core Commands")
    def do_show(self, entry_id: cmd2.Statement):
        """Show a specific entry by ID"""
        if self.active_dicts is None:
            self.perror("Please select a dictionary first.")
        else:
            for active_dict in self.active_dicts:
                try:
                    result = active_dict.entry(entry_id)
                    self.poutput(
                        result.transliterate(
                            scheme=self.output_scheme,
                            transliterate_keys=active_dict.transliterate_keys
                        )
                    )
                    # self.logger.debug(f"Data: {result.data}")
                except Exception:
                    result = None

                if result is None:
                    self.perror(
                        f"Entry {entry_id} not found in '{active_dict.id}'."
                    )

    # ----------------------------------------------------------------------- #



    @cmd2.with_category("CDSL Core Commands")
    def do_search(self, line: cmd2.Statement):
        """
        Search in the active dictionaries

        Note
        ----
        * Searching in the active dictionaries is also the default action.
        * In general, we do not need to use this command explicitly unless we
          want to search the command keywords, such as, `available` `search`,
          `version`, `help` etc. in the active dictionaries.
        """
        if self.active_dicts is None:
            self.perror("Please select a dictionary first.")
        else:
            for active_dict in self.active_dicts:
                search_pattern = transliterate(
                    line, self.input_scheme, INTERNAL_SCHEME
                ) if active_dict.transliterate_keys else line
                results = active_dict.search(
                    search_pattern,
                    mode=self.search_mode,
                    limit=self.limit
                )
                if not results:
                    continue

                self.poutput(
                    f"\nFound {len(results)} results in {active_dict.id}.\n"
                )
                for result in results:
                    self.poutput(
                        result.transliterate(
                            scheme=self.output_scheme,
                            transliterate_keys=active_dict.transliterate_keys
                        )
                    )

    # ----------------------------------------------------------------------- #

    def default(self, statement: cmd2.Statement):
        self.do_search(statement.raw)

    # ----------------------------------------------------------------------- #

    def cmdloop(self, intro: cmd2.Statement = None):
        self.poutput(self.intro)
        self.poutput(self.desc)
        self.cdsl.setup(dict_ids=self.dict_ids)

        self.poutput(f"Loaded {len(self.cdsl.dicts)} dictionaries.")

        if self.dict_ids is not None:
            self.do_use(" ".join(self.dict_ids))

        while True:
            try:
                super(self.__class__, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                self.poutput("\nKeyboardInterrupt")

    # ----------------------------------------------------------------------- #

    def do_version(self, _: cmd2.Statement):
        """Show the current version of PyCDSL"""
        self.poutput(f"PyCDSL v{__version__}")

###############################################################################
