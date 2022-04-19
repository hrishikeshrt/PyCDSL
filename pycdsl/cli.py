#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Console script for PyCDSL"""

###############################################################################

import sys
import logging
import argparse

from .corpus import CDSLCorpus
from .shell import CDSLShell
from .constants import (
    DEFAULT_SCHEME,
    DEFAULT_SEARCH_MODE,
    DEFAULT_HISTORY_FILE,
    DEFAULT_STARTUP_SCRIPT
)
from . import __version__

###############################################################################

ROOT_LOGGER = logging.getLogger()
if not ROOT_LOGGER.hasHandlers():
    ROOT_LOGGER.addHandler(logging.StreamHandler())
ROOT_LOGGER.setLevel(logging.INFO)

###############################################################################


def main():
    """Command Line Interface for PyCDSL"""
    description = (
        "Access dictionaries from Cologne Digital Sanskrit Lexicon (CDSL)"
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="start in an interactive REPL mode"
    )
    parser.add_argument(
        "-s",
        "--search",
        help="search pattern (ignored if `--interactive` mode is set)"
    )
    parser.add_argument(
        "-p",
        "--path",
        help="path to installation"
    )
    parser.add_argument(
        "-d",
        "--dicts",
        nargs="+",
        help="dictionary id(s)"
    )
    parser.add_argument(
        "-sm",
        "--search-mode",
        default=DEFAULT_SEARCH_MODE,
        help="search mode"
    )
    parser.add_argument(
        "-is",
        "--input-scheme",
        default=DEFAULT_SCHEME,
        help="input transliteration scheme"
    )
    parser.add_argument(
        "-os",
        "--output-scheme",
        default=DEFAULT_SCHEME,
        help="output transliteration scheme"
    )
    parser.add_argument(
        "-hf",
        "--history-file",
        default=DEFAULT_HISTORY_FILE,
        help="path to the history file"
    )
    parser.add_argument(
        "-sc",
        "--startup-script",
        default=DEFAULT_STARTUP_SCRIPT,
        help="path to the startup script"
    )
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="update specified dictionaries"
    )
    parser.add_argument(
        "-dbg",
        "--debug",
        action="store_true",
        help="turn debug mode on"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="show version and exit"
    )

    args = vars(parser.parse_args())

    # arguments
    data_dir = args.get("path")
    dict_ids = args.get("dicts")
    search_mode = args.get("search_mode")
    input_scheme = args.get("input_scheme")
    output_scheme = args.get("output_scheme")

    history_file = args.get("history_file")
    startup_script = args.get("startup_script")

    flag_update = args.get("update")
    flag_debug = args.get("debug")
    flag_interactive = args.get("interactive")

    search_pattern = args.get("search")

    # debug
    if flag_debug:
        ROOT_LOGGER.setLevel(logging.DEBUG)

    if flag_interactive:
        # interactive
        cdsl_shell = CDSLShell(
            data_dir=data_dir,
            dict_ids=dict_ids,
            search_mode=search_mode,
            input_scheme=input_scheme,
            output_scheme=output_scheme,
            history_file=history_file,
            startup_script=startup_script
        )
        cdsl_shell.cdsl.setup(dict_ids=dict_ids, update=flag_update)
        return cdsl_shell.cmdloop()
    else:
        # non-interactive shell command
        cdsl = CDSLCorpus(
            data_dir=data_dir,
            search_mode=search_mode,
            input_scheme=input_scheme,
            output_scheme=output_scheme
        )
        cdsl.setup(dict_ids=dict_ids, update=flag_update)

        if not flag_update and not search_pattern:
            print("Must specify a search pattern in non-interactive mode.")
            parser.print_help()
            return 1

        # search
        if search_pattern:
            all_results = cdsl.search(pattern=search_pattern)
            for dict_id, dict_results in all_results.items():
                n_results = len(dict_results)
                print(
                    "\n"
                    f"Found {n_results} results in the dictionary '{dict_id}'."
                    "\n"
                )
                for result in dict_results:
                    print(result)

    return 0

###############################################################################


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
