"""Console script for PyCDSL"""

import sys
import argparse

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from .pycdsl import CDSLCorpus, INTERNAL_SCHEME, DEFAULT_SCHEME
from .shell import CDSLShell
from .utils import validate_scheme
from . import __version__

###############################################################################


def main():
    """Command Line Interface for PyCDSL"""
    parser = argparse.ArgumentParser("CLI for PyCDSL")
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
    args = vars(parser.parse_args())
    print(args)

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
            print("Must specify a search pattern in non-interactive mode.")
            parser.print_help()
            return 1

        cdsl = CDSLCorpus(
            data_dir=args.get("path"),
            input_scheme=args.get("input_scheme"),
            output_scheme=args.get("output_scheme")
        )
        cdsl.setup(args.get("dicts"), update=args.get("update"))
        active_dict = next(iter(cdsl.dicts))
        for result in cdsl.dicts[active_dict].search(args.get("search")):
            print(result)

    return 0

###############################################################################


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
