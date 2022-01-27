"""Console script for PyCDSL"""

import os
import cmd
import sys

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

from .pycdsl import CDSLCorpus

###############################################################################

DEFAULT_DICTIONARIES = [
    # Sanskrit-English
    # ----------------
    "MW", "AP90",
    # "WIL", "YAT", "GST", "MW72", "BEN", "LAN", "CAE", "MD", "SHS",

    # English-Sanskrit
    # ----------------
    "MWE", "AE",  # "BOR",

    # Sanskrit-Sanskrit
    # -----------------
    # "VCP", "SKD", "ARMH",

    # Special
    # ---------
    # "INM", "MCI", "VEI" "PUI", "PE", "SNP",
]

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
    intro = "Cologne Sanskrit Digital Lexicon (CDSL)"
    desc = "Type any keyword to search in the selected lexicon." \
           " (help or ? for list of options)"
    prompt = "(CDSL::None) "

    def __init__(self, data_dir=None, dict_ids=None):
        super(self.__class__, self).__init__()
        self.debug = False
        self.schemes = [
            sanscript.HK,
            sanscript.VELTHUIS,
            sanscript.ITRANS,
            sanscript.SLP1,
            sanscript.WX,
            sanscript.DEVANAGARI
        ]
        self.input_scheme = sanscript.DEVANAGARI

        self.cdsl = CDSLCorpus(data_dir=data_dir)
        self.dict_ids = dict_ids or DEFAULT_DICTIONARIES
        self.active = None
        self.dict = None

    # ----------------------------------------------------------------------- #
    # Debug Mode

    def do_debug(self, arg):
        """Turn debug mode on/off"""
        if arg.lower() in ["true", "on", "yes"]:
            self.debug = True
        if arg.lower() in ["false", "off", "no"]:
            self.debug = False
        print(f"Debug: {self.debug}")

    # ----------------------------------------------------------------------- #
    # Input Transliteration Scheme

    def complete_scheme(self, text, line, begidx, endidx):
        return [sch for sch in self.schemes if sch.startswith(text)]

    def do_scheme(self, scheme):
        """Change the input transliteration scheme"""
        if not scheme:
            print(f"Input scheme: {self.input_scheme}")
        else:
            if scheme not in self.schemes:
                print(f"Invalid scheme. (valid schemes are {self.schemes}")
            else:
                self.input_scheme = scheme
                print(f"Input scheme: {self.input_scheme}")

    # ----------------------------------------------------------------------- #

    def do_available(self, dict_id):
        """Display available lexicons"""
        for _, cdsl_dict in self.cdsl.available_dicts.items():
            print(cdsl_dict)

    def do_use(self, dict_id):
        """Use a specific lexicon"""
        dict_id = dict_id.upper()
        status = (dict_id in self.cdsl._dicts) or self.cdsl.setup([dict_id])
        if status:
            self.active = dict_id
            self.prompt = f"(CDSL::{self.active}) "
            self.dict = self.cdsl._dicts[dict_id]
        else:
            print(f"Couldn't setup dictionary '{dict_id}'.")

    # ----------------------------------------------------------------------- #

    def default(self, line):
        if self.dict is None:
            print("Please select a dictionary first.")
        else:
            search_key = line if self.dict.english_keys else transliterate(
                line, self.input_scheme, sanscript.DEVANAGARI
            )
            results = self.dict.search(search_key)[:50]
            for result in results:
                print(result)

    def cmdloop(self, intro=None):
        print(self.intro)
        print(self.desc)
        self.cdsl.setup(dict_ids=self.dict_ids)
        while True:
            try:
                super(self.__class__, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")


def main():
    """Shell Interface for PyCDSL"""
    cdsl = CDSLShell()
    cdsl.cmdloop()

###############################################################################


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
