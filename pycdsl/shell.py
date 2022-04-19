#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REPL Shell for PyCDSL"""

###############################################################################

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
        super().__init__(
            persistent_history_file=history_file,
            startup_script=startup_script,
            allow_cli_args=False
        )
        self.default_category = "Utility"
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

    # ----------------------------------------------------------------------- #

    def _limit_handler(self, name, old_value, new_value):
        if new_value < 0:
            self.limit = None

    # ----------------------------------------------------------------------- #
    # Dictionary Information

    @cmd2.with_category("Core")
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

    @cmd2.with_category("Core")
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

    @cmd2.with_category("Core")
    def do_dicts(self, _: cmd2.Statement):
        """Display a list of dictionaries available locally"""
        for _, cdsl_dict in self.cdsl.dicts.items():
            self.poutput(cdsl_dict)

    @cmd2.with_category("Core")
    def do_available(self, _: cmd2.Statement):
        """Display a list of dictionaries available in CDSL"""
        for _, cdsl_dict in self.cdsl.available_dicts.items():
            self.poutput(cdsl_dict)

    # ----------------------------------------------------------------------- #

    @cmd2.with_category("Core")
    def do_update(self, _: cmd2.Statement):
        """Update loaded dictionaries"""
        self.cdsl.setup(list(self.cdsl.dicts), update=True)

    # ----------------------------------------------------------------------- #

    def _use_completer(self, text, line, begidx, endidx):
        return [
            dict_id
            for dict_id in self.cdsl.available_dicts
            if dict_id.startswith(text.upper())
        ]
    use_parser = cmd2.Cmd2ArgumentParser()
    use_parser.add_argument(
        "dict_ids",
        nargs="*",
        type=str.upper,
        help="Dictionary IDs",
        completer=_use_completer
    )
    use_parser.add_argument(
        "-a", "--all", action="store_true", help="Load all"
    )
    use_parser.add_argument(
        "-n", "--none", action="store_true", help="Unload all"
    )

    @cmd2.with_category("Core")
    @cmd2.with_argparser(use_parser)
    def do_use(self, namespace: cmd2.argparse.Namespace):
        """
        Load the specified dictionaries from CDSL.
        If not available locally, they will be installed first.
        """
        if namespace.all:
            status = self.cdsl.setup()
            if status:
                self.active_dicts = self.cdsl.dicts.values()
            else:
                self.perror("Couldn't setup some dictionaries.")
        elif namespace.none:
            self.active_dicts = []
        else:
            dict_ids = namespace.dict_ids
            if not dict_ids:
                self.perror("Please provide dictionary ID(s) to use.")
                return

            self.active_dicts = []
            for dict_id in dict_ids:
                status = (
                    dict_id in self.cdsl.dicts
                ) or self.cdsl.setup([dict_id])
                if status:
                    self.active_dicts.append(self.cdsl.dicts[dict_id])
                else:
                    self.perror(f"Couldn't setup dictionary '{dict_id}'.")

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

    show_parser = cmd2.Cmd2ArgumentParser()
    show_parser.add_argument("entry_id", type=int, help="entry ID to show")
    show_parser.add_argument(
        "--show-data", action="store_true", help="show XML data field"
    )

    @cmd2.with_category("Core")
    @cmd2.with_argparser(show_parser)
    def do_show(self, namespace: cmd2.argparse.Namespace):
        """Show a specific entry by ID"""
        if self.active_dicts is None:
            self.perror("Please select a dictionary first.")
        else:
            entry_id = namespace.entry_id
            show_data = namespace.show_data
            for active_dict in self.active_dicts:
                try:
                    result = active_dict.entry(entry_id)
                    self.poutput(
                        result.transliterate(
                            scheme=self.output_scheme,
                            transliterate_keys=active_dict.transliterate_keys
                        )
                    )
                    if show_data:
                        self.poutput(f"\nData:\n{result.data}")
                except Exception:
                    result = None

                if result is None:
                    self.perror(
                        f"Entry {entry_id} not found in '{active_dict.id}'."
                    )

    # ----------------------------------------------------------------------- #

    search_parser = cmd2.Cmd2ArgumentParser()
    search_parser.add_argument("pattern", type=str, help="search pattern")
    search_parser.add_argument("--limit", type=int, help="limit results")
    search_parser.add_argument("--offset", type=int, help="skip results")

    @cmd2.with_category("Core")
    @cmd2.with_argparser(search_parser)
    def do_search(self, namespace: cmd2.argparse.Namespace):
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
            pattern = namespace.pattern
            offset = namespace.offset
            limit = namespace.limit or self.limit

            for active_dict in self.active_dicts:
                search_pattern = transliterate(
                    pattern, self.input_scheme, INTERNAL_SCHEME
                ) if active_dict.transliterate_keys else pattern
                results = active_dict.search(
                    search_pattern,
                    mode=self.search_mode,
                    limit=limit,
                    offset=offset
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
