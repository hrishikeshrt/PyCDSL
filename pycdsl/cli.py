#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Console script for PyCDSL"""

###############################################################################

import sys
import logging
import argparse

from .corpus import CDSLCorpus
from .shell import CDSLShell
from .constants import DEFAULT_SCHEME
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
        help="Start in an interactive REPL mode"
    )
    parser.add_argument(
        "-s",
        "--search",
        help="Search pattern. Ignored if `--interactive` mode is set."
    )
    parser.add_argument(
        "-p",
        "--path",
        help="Path to installation"
    )
    parser.add_argument(
        "-d",
        "--dicts",
        nargs="+",
        help="Dictionary IDs"
    )
    parser.add_argument(
        "-is",
        "--input-scheme",
        default=DEFAULT_SCHEME,
        help="Input transliteration scheme"
    )
    parser.add_argument(
        "-os",
        "--output-scheme",
        default=DEFAULT_SCHEME,
        help="Output transliteration scheme"
    )
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Update the specified dictionaries."
    )
    parser.add_argument(
        "-dbg",
        "--debug",
        action="store_true",
        help="Turn debug mode on."
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show version and exit."
    )

    args = vars(parser.parse_args())

    if args.get('debug'):
        ROOT_LOGGER.setLevel(logging.DEBUG)

    if args.get("interactive"):
        cdsl_shell = CDSLShell(
            data_dir=args.get("path"),
            dict_ids=args.get("dicts"),
            input_scheme=args.get("input_scheme"),
            output_scheme=args.get("output_scheme")
        )
        if args.get("update"):
            cdsl_shell.cdsl.setup(dict_ids=args.get("dicts"), update=True)
        cdsl_shell.cmdloop()
    else:
        if not args.get("search"):
            ROOT_LOGGER.error(
                "Must specify a search pattern in non-interactive mode."
            )
            parser.print_help()
            return 1

        cdsl = CDSLCorpus(
            data_dir=args.get("path"),
            input_scheme=args.get("input_scheme"),
            output_scheme=args.get("output_scheme")
        )

        cdsl.setup(args.get("dicts"), update=args.get("update"))
        all_results = cdsl.search(
            pattern=args.get("search"),
            dict_ids=args.get("dicts"),
        )
        for dict_id, dict_results in all_results.items():
            result_count = len(dict_results)
            print(
                "\n"
                f"Found {result_count} results in the dictionary '{dict_id}'."
                "\n"
            )
            for result in dict_results:
                print(result)

    return 0

###############################################################################


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
