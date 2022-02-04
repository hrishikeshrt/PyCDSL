"""Console script for PyCDSL"""

import os
import cmd
import sys
import logging

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from .pycdsl import CDSLCorpus, INTERNAL_SCHEME, DEFAULT_SCHEME
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
    intro = "Cologne Sanskrit Digital Lexicon (CDSL)\n" \
            "---------------------------------------"
    desc = "Install or load a lexicon by typing `use <DICT_ID>` " \
           "e.g. `use MW`.\n" \
           "Type any keyword to search in the selected lexicon. " \
           "(help or ? for list of options)"
    prompt = "(CDSL::None) "

    def __init__(self, data_dir=None, dict_ids=None):
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
        self.input_scheme = sanscript.DEVANAGARI

        self.input_scheme = DEFAULT_SCHEME
        self.output_scheme = DEFAULT_SCHEME

        self.cdsl = CDSLCorpus(data_dir=data_dir, scheme=None)
        self.dict_ids = dict_ids
        self.active = None

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
        """Display information about the active dictionary"""
        if self.active is None:
            self.logger.error("Please select a dictionary first.")
        else:
            print(self.active)

    def do_dicts(self, text=None):
        """Display a list of lexicon available locally"""
        for _, cdsl_dict in self.cdsl.dicts.items():
            print(cdsl_dict)

    def do_available(self, text=None):
        """Display lexicons available in CDSL"""
        for _, cdsl_dict in self.cdsl.available_dicts.items():
            print(cdsl_dict)

    # ----------------------------------------------------------------------- #

    def do_update(self, text):
        """Update loaded dictionaries"""
        self.cdsl.setup(list(self.cdsl.dicts), update=True)

    # ----------------------------------------------------------------------- #

    def complete_use(self, text, line, begidx, endidx):
        return [
            dict_id
            for dict_id in self.cdsl.available_dicts
            if dict_id.startswith(text.upper())
        ]

    def do_use(self, dict_id):
        """Install/Load a specific lexicon from CDSL."""
        dict_id = dict_id.upper()
        status = (dict_id in self.cdsl.dicts) or self.cdsl.setup([dict_id])
        if status:
            self.active = self.cdsl.dicts[dict_id]
            self.prompt = f"(CDSL::{self.active.id}) "
        else:
            self.logger.error(f"Couldn't setup dictionary '{dict_id}'.")

    # ----------------------------------------------------------------------- #

    def do_show(self, entry_id):
        """Show a specific entry by ID"""
        if self.active is None:
            self.logger.error("Please select a dictionary first.")
        else:
            result = self.active.entry(entry_id)
            print(
                result.transliterate(
                    scheme=self.output_scheme,
                    transliterate_key=self.active.transliterate_keys
                )
            )
            self.logger.debug(f"Data: {result.data}")

    # ----------------------------------------------------------------------- #

    def do_version(self, text):
        """Show the current version of PyCDSL"""
        print(__version__)

    # ----------------------------------------------------------------------- #

    def default(self, line):
        if self.active is None:
            self.logger.error("Please select a dictionary first.")
        else:
            search_key = transliterate(
                line, self.input_scheme, INTERNAL_SCHEME
            ) if self.active.transliterate_keys else line
            results = self.active.search(search_key)[:50]
            for result in results:
                print(
                    result.transliterate(
                        scheme=self.output_scheme,
                        transliterate_keys=self.active.transliterate_keys
                    )
                )

    def cmdloop(self, intro=None):
        print(self.intro)
        print(self.desc)
        self.cdsl.setup(dict_ids=self.dict_ids)

        print(f"Loaded {len(self.cdsl.dicts)} dictionaries.")

        while True:
            try:
                super(self.__class__, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")


###############################################################################


def main():
    """Shell Interface for PyCDSL"""
    cdsl = CDSLShell()
    cdsl.cmdloop()

###############################################################################


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
