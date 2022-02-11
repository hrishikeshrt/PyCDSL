======
PyCDSL
======


.. image:: https://img.shields.io/pypi/v/PyCDSL?color=success
        :target: https://pypi.python.org/pypi/PyCDSL

.. image:: https://readthedocs.org/projects/pycdsl/badge/?version=latest
        :target: https://pycdsl.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/PyCDSL
        :target: https://pypi.python.org/pypi/PyCDSL
        :alt: Python Version Support

.. image:: https://img.shields.io/github/issues/hrishikeshrt/PyCDSL
        :target: https://github.com/hrishikeshrt/PyCDSL/issues
        :alt: GitHub Issues

.. image:: https://img.shields.io/github/followers/hrishikeshrt?style=social
        :target: https://github.com/hrishikeshrt
        :alt: GitHub Followers

.. image:: https://img.shields.io/twitter/follow/hrishikeshrt?style=social
        :target: https://twitter.com/hrishikeshrt
        :alt: Twitter Followers


PyCDSL is a python interface to `Cologne Digital Sanskrit Lexicon (CDSL)`_.

.. _`Cologne Digital Sanskrit Lexicon (CDSL)`: https://www.sanskrit-lexicon.uni-koeln.de/


* Free software: GNU General Public License v3
* Documentation: https://pycdsl.readthedocs.io.


Features
========

* CDSL Corpus Management (Download, Update, Access)
* Unified Programmable Interface to access all dictionaries available at CDSL
* Console Command and REPL Interface for easy dictionary search
* Extensive support for transliteration using :code:`indic-transliteration` module


Usage
=====

PyCDSL can be used in a python project, as a console command and
as an interactive REPL interface.

Using PyCDSL in a Project
-------------------------

Import PyCDSL in a project:

.. code-block:: python

    import pycdsl

Create a CDSLCorpus Instance:

.. code-block:: python

    # Default installation at ~/cdsl_data
    CDSL = pycdsl.CDSLCorpus()

    # Custom installation path can be specified with argument `data_dir`
    # e.g. CDSL = pycdsl.CDSLCorpus(data_dir="custom-installation-path")

    # Custom transliteration schemes for input and output can be specified
    # with arguments `input_scheme` and `output_scheme`.
    # Values should be valid names of the schemes from `indic-transliteration`
    # If unspecified, `DEFAULT_SCHEME` (`devanagari`) would be used.

    CDSL = pycdsl.CDSLCorpus(input_scheme="itrans", output_scheme="iast")

Setup default dictionaries (:code:`["MW", "MWE", "AP90", "AE"]`):

.. code-block:: python

    # Note: Any additional dictionaries that are installed will also be loaded.
    CDSL.setup()

    # For loading specific dictionaries only,
    # a list of dictionary IDs can be passed to the setup function
    # e.g. CDSL.setup(["VCP"])

    # If `update` flag is True, update check is performed for every dictionary
    # in `dict_ids` and if available, the updated version is installed
    # e.g. CDSL.setup(["MW"], update=True)

Search in a dictionary:

.. code-block:: python

    # Any loaded dictionary is accessible through `dicts` using dictionary ID
    # e.g. CDSL.dicts["MW"]
    results = CDSL.dicts["MW"].search("राम")

    # Alternatively, they are also accessible like an attribute
    # e.g. CDSL.MW, CDSL.MWE etc.
    results = CDSL.MW.search("राम")

    # Note: Attribute access actually uses the `dicts` property under the hood
    # to access the dictionaries.
    # >>> CDSL.MW is CDSL.dicts["MW"]
    # True

    # `input_scheme` and `output_scheme` can be specified to the search function.
    CDSL.MW.search("kṛṣṇa", input_scheme="iast", output_scheme="itrans")[0]
    # <MWEntry: 55142: kRRiShNa = 1. kRRiShNa/ mf(A/)n. black, dark, dark-blue (opposed to shveta/, shukla/, ro/hita, and aruNa/), RV.; AV. &c.>

    # Search using wildcard (i.e. `*`)
    # e.g. To search all etnries starting with kRRi (i.e. कृ)
    CDSL.MW.search("kRRi*", input_scheme="itrans")

    # Limit and/or Offset the number of search results, e.g.
    # Show the first 10 results
    CDSL.MW.search("kṛ*", input_scheme="iast", limit=10)
    # Show the next 10 results
    CDSL.MW.search("kṛ*", input_scheme="iast", limit=10, offset=10)

Access an entry by ID:

.. code-block:: python

    entry = CDSL.MW.entry("263938")

    # >>> entry
    # <MWEntry: 263938: हृषीकेश = lord of the senses (said of Manas), BhP.>

    # Output transliteration scheme can also be provided

    CDSL.MW.entry("263938", output_scheme="iast")
    # <MWEntry: 263938: hṛṣīkeśa = lord of the senses (said of Manas), BhP.>

:code:`Entry` class also supports transliteration after creation.
Thus, any entry fetched either through :code:`search()` function or through :code:`entry()` function can be transliterated.

Transliterate a single entry:

.. code-block:: python

    CDSL.MW.entry("263938").transliterate("slp1")
    # <MWEntry: 263938: hfzIkeSa = lord of the senses (said of Manas), BhP.>

Change transliteration scheme for a dictionary:

.. code-block:: python

    CDSL.MW.set_scheme(input_scheme="itrans")
    CDSL.MW.search("rAma")

**Note**: Please check the documentation of modules in the PyCDSL Package for more
detailed information on available classes and functions.

https://pycdsl.readthedocs.io/en/latest/pycdsl.html


Using Console Interface of PyCDSL
---------------------------------

Help to the Console Interface:

.. code-block:: console

    usage: cdsl [-h] [-i] [-s SEARCH] [-p PATH] [-d DICTS [DICTS ...]]
                [-is INPUT_SCHEME] [-os OUTPUT_SCHEME] [-u] [-dbg] [-v]

    Access dictionaries from Cologne Digital Sanskrit Lexicon (CDSL)

    optional arguments:
    -h, --help          show this help message and exit
    -i, --interactive   Start in an interactive REPL mode
    -s SEARCH, --search SEARCH
                        Search pattern. Ignored if `--interactive` mode is set.
    -p PATH, --path PATH  Path to installation
    -d DICTS [DICTS ...], --dicts DICTS [DICTS ...]
                        Dictionary IDs
    -is INPUT_SCHEME, --input-scheme INPUT_SCHEME
                        Input transliteration scheme
    -os OUTPUT_SCHEME, --output-scheme OUTPUT_SCHEME
                        Output transliteration scheme
    -u, --update        Update the specified dictionaries.
    -dbg, --debug       Turn debug mode on.
    -v, --version       Show version and exit.


**Note**: Arguments for specifying installation path, dictionary IDs, input and output transliteration schemes
are valid for both interactive REPL shell and non-interactive console command.

Using REPL Interface of PyCDSL
------------------------------

To use REPL Interface to Cologne Digital Sanskrit Lexicon (CDSL):

.. code-block:: console

    $ cdsl -i


REPL Session Example
--------------------

.. code-block:: console

    Cologne Sanskrit Digital Lexicon (CDSL)
    ---------------------------------------
    Install or load dictionaries by typing `use [DICT_IDS..]` e.g. `use MW`.
    Type any keyword to search in the selected dictionaries. (help or ? for list of options)
    Loaded 4 dictionaries.

    (CDSL::None) help

    Documented commands (type help <topic>):
    ========================================
    EOF        debug  exit  info          limit          shell  update  version
    available  dicts  help  input_scheme  output_scheme  show   use

    (CDSL::None) help available
    Display a list of dictionaries available in CDSL

    (CDSL::None) help dicts
    Display a list of dictionaries available locally

    (CDSL::None) dicts
    CDSLDict(id='AP90', date='1890', name='Apte Practical Sanskrit-English Dictionary')
    CDSLDict(id='MW', date='1899', name='Monier-Williams Sanskrit-English Dictionary')
    CDSLDict(id='MWE', date='1851', name='Monier-Williams English-Sanskrit Dictionary')
    CDSLDict(id='AE', date='1920', name="Apte Student's English-Sanskrit Dictionary")

    (CDSL::None) update
    Data for dictionary 'AP90' is up-to-date.
    Data for dictionary 'MW' is up-to-date.
    Data for dictionary 'MWE' is up-to-date.
    Data for dictionary 'AE' is up-to-date.

    (CDSL::None) use MW
    Using 1 dictionaries: ['MW']

    (CDSL::MW) हृषीकेश

    Found 6 results in MW.

    <MWEntry: 263922: हृषीकेश = हृषी-केश a   See below under हृषीक.>
    <MWEntry: 263934: हृषीकेश = हृषीकेश b m. (perhaps = हृषी-केश cf. हृषी-वत् above) id. (-त्व n.), MBh.; Hariv. &c.>
    <MWEntry: 263935: हृषीकेश = N. of the tenth month, VarBṛS.>
    <MWEntry: 263936: हृषीकेश = of a Tīrtha, Cat.>
    <MWEntry: 263937: हृषीकेश = of a poet, ib.>
    <MWEntry: 263938: हृषीकेश = lord of the senses (said of Manas), BhP.>

    (CDSL::MW) show 263938

    <MWEntry: 263938: हृषीकेश = lord of the senses (said of Manas), BhP.>

    (CDSL::MW) input_scheme itrans
    Input scheme: itrans

    (CDSL::MW) hRRiSIkesha

    Found 6 results in MW.

    <MWEntry: 263922: हृषीकेश = हृषी-केश a   See below under हृषीक.>
    <MWEntry: 263934: हृषीकेश = हृषीकेश b m. (perhaps = हृषी-केश cf. हृषी-वत् above) id. (-त्व n.), MBh.; Hariv. &c.>
    <MWEntry: 263935: हृषीकेश = N. of the tenth month, VarBṛS.>
    <MWEntry: 263936: हृषीकेश = of a Tīrtha, Cat.>
    <MWEntry: 263937: हृषीकेश = of a poet, ib.>
    <MWEntry: 263938: हृषीकेश = lord of the senses (said of Manas), BhP.>

    (CDSL::MW) output_scheme iast
    Output scheme: iast

    (CDSL::MW) hRRiSIkesha

    <MWEntry: 263922: hṛṣīkeśa = hṛṣī-keśa a   See below under hṛṣīka.>
    <MWEntry: 263934: hṛṣīkeśa = hṛṣīkeśa b m. (perhaps = hṛṣī-keśa cf. hṛṣī-vat above) id. (-tva n.), MBh.; Hariv. &c.>
    <MWEntry: 263935: hṛṣīkeśa = N. of the tenth month, VarBṛS.>
    <MWEntry: 263936: hṛṣīkeśa = of a Tīrtha, Cat.>
    <MWEntry: 263937: hṛṣīkeśa = of a poet, ib.>
    <MWEntry: 263938: hṛṣīkeśa = lord of the senses (said of Manas), BhP.>

    (CDSL::MW) limit 2
    Limit: 2

    (CDSL::MW) hRRiSIkesha

    Found 2 results in MW.

    <MWEntry: 263922: hṛṣīkeśa = hṛṣī-keśa a   See below under hṛṣīka.>
    <MWEntry: 263934: hṛṣīkeśa = hṛṣīkeśa b m. (perhaps = hṛṣī-keśa cf. hṛṣī-vat above) id. (-tva n.), MBh.; Hariv. &c.>

    (CDSL::MW) info
    Total 1 dictionaries are active.
    CDSLDict(id='MW', date='1899', name='Monier-Williams Sanskrit-English Dictionary')

    (CDSL::MW) use WIL

    Downloading 'WIL.web.zip' ... (8394727 bytes)
    100%|██████████████████████████████████████████████████████████████████████████████████████| 8.39M/8.39M [00:21<00:00, 386kB/s]
    Successfully downloaded 'WIL.web.zip' from 'https://www.sanskrit-lexicon.uni-koeln.de/scans/WILScan/2020/downloads/wilweb1.zip'.
    Using 1 dictionaries: ['WIL']

    (CDSL::WIL)

    (CDSL::WIL) use WIL MW
    Using 2 dictionaries: ['WIL', 'MW']

    (CDSL::WIL,MW) hRRiSIkesha

    Found 1 results in WIL.

    <WILEntry: 44411: hṛṣīkeśa = hṛṣīkeśa  m. (-śaḥ) KṚṢṆA or VIṢṆU. E. hṛṣīka an organ of sense, and īśa lord.>

    Found 6 results in MW.

    <MWEntry: 263922: hṛṣīkeśa = hṛṣī-keśa a   See below under hṛṣīka.>
    <MWEntry: 263934: hṛṣīkeśa = hṛṣīkeśa b m. (perhaps = hṛṣī-keśa cf. hṛṣī-vat above) id. (-tva n.), MBh.; Hariv. &c.>
    <MWEntry: 263935: hṛṣīkeśa = N. of the tenth month, VarBṛS.>
    <MWEntry: 263936: hṛṣīkeśa = of a Tīrtha, Cat.>
    <MWEntry: 263937: hṛṣīkeśa = of a poet, ib.>
    <MWEntry: 263938: hṛṣīkeśa = lord of the senses (said of Manas), BhP.>

    (CDSL::WIL,MW) use MW WIL AP90 MWE AE
    Using 5 dictionaries: ['MW', 'WIL', 'AP90', 'MWE', 'AE']

    (CDSL::MW+4) exit

    Bye


Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

