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
    # e.g. CDSL = pycdsl.CDSLCorpus(data_dir='custom-installation-path')

    # Custom transliteration schemes for input and output can be specified
    # with arguments `input_scheme` and `output_scheme`.
    # Values should be valid names of the schemes from `indic-transliteration`
    # If unspecified, `DEFAULT_SCHEME` (`devanagari`) would be used.

    CDSL = pycdsl.CDSLCorpus(input_scheme='itrans', output_scheme='iast')

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
    CDSL.MW.search('kṛṣṇa', input_scheme='iast', output_scheme='itrans')[0]
    # <MWEntry: 55142: kRRiShNa = 1. kRRiShNa/ mf(A/)n. black, dark, dark-blue (opposed to shveta/, shukla/, ro/hita, and aruNa/), RV.; AV. &c.>

Access an entry by ID:

.. code-block:: python

    entry = CDSL.MW.entry("263938")

    # >>> entry
    # <MWEntry: 263938: हृषीकेश = lord of the senses (said of Manas), BhP.>

    # Output transliteration scheme can also be provided

    CDSL.MW.entry("263938", output_scheme='iast')
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

    usage: CLI for PyCDSL [-h] [-i] [-s SEARCH] [-p PATH] [-d DICTS [DICTS ...]] [-is INPUT_SCHEME] [-os OUTPUT_SCHEME] [-u] [-dbg]

    optional arguments:
    -h, --help            show this help message and exit
    -i, --interactive     Start in an interactive REPL mode
    -s SEARCH, --search SEARCH
                            Search pattern. Ignored if `--interactive` mode is set.
    -p PATH, --path PATH  Path to installation
    -d DICTS [DICTS ...], --dicts DICTS [DICTS ...]
                            Dictionary IDs
    -is INPUT_SCHEME, --input-scheme INPUT_SCHEME
                            Input transliteration scheme
    -os OUTPUT_SCHEME, --output-scheme OUTPUT_SCHEME
                            Output transliteration scheme
    -u, --update          Update the specified dictionaries.
    -dbg, --debug         Turn debug mode on.


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
    Install or load a lexicon by typing `use <DICT_ID>` e.g. `use MW`.
    Type any keyword to search in the selected lexicon. (help or ? for list of options)
    Loaded 4 dictionaries.

    (CDSL::None) help

    Documented commands (type help <topic>):
    ========================================
    EOF        debug  exit  info          output_scheme  show    use
    available  dicts  help  input_scheme  shell          update  version

    (CDSL::None) help available
    Display lexicons available in CDSL

    (CDSL::None) help dicts
    Display a list of lexicon available locally

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
    (CDSL::MW) हृषीकेश

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

    (CDSL::MW) info

    CDSLDict(id='MW', date='1899', name='Monier-Williams Sanskrit-English Dictionary')

    (CDSL::MW) exit

    Bye

