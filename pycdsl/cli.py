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
        action='store_true',
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
        nargs='+',
        help="Dictionary IDs"
    )
    parser.add_argument(
        "-is",
        "--input-scheme",
        help="Input transliteration scheme"
    )
    parser.add_argument(
        "-os",
        "--output-scheme",
        help="Output transliteration scheme"
    )
    args = vars(parser.parse_args())

    if args['interactive']:
        cdsl_shell = CDSLShell(
            data_dir=args.get('path'),
            dict_ids=args.get('dicts'),
            input_scheme=args.get('input-scheme'),
            output_scheme=args.get('output-scheme')
        )
        cdsl_shell.cmdloop()
    else:
        if not args.get('search'):
            parser.print_help()
            return 1

        cdsl = CDSLCorpus(
            data_dir=args.get('path'),
            scheme=None
        )
        cdsl.setup(args.get('dicts'))
        active_dict = list(cdsl.dicts)[0]
        for result in cdsl.dicts[active_dict].search(args.get('search')):
            print(result)

    return 0

###############################################################################


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
