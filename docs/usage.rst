=====
Usage
=====

PyCDSL can be used in a project for programmatic access as well as from the shell
as a REPL interface.

Using PyCDSL in a Project
=========================

To use PyCDSL in a project::

    import pycdsl

Create a CDSLCorpus Instance::

    # Default installation at ~/cdsl_data
    CDSL = pycdsl.CDSLCorpus()

    # Custom installation path can be specified with argument `data_dir`
    # e.g. CDSL = pycdsl.CDSLCorpus(data_dir='custom-installation-path')

    # Custom transliteration scheme can be specified with argument `scheme`
    # `scheme` is a valid name of the scheme from `indic-transliteration`
    CDSL = pycdsl.CDSLCorpus(scheme='itrans')

Setup default dictionaries (:code:`["MW", "MWE", "AP90", "AE"]`)::

    # Note: Any additional dictionaries that are installed will also be loaded.
    CDSL.setup()

    # For loading specific dictionaries only,
    # a list of dictionary IDs can be passed to the setup function
    # e.g. CDSL.setup(["VCP"])

    # If `update` flag is True, update check is performed for every dictionary
    # in `dict_ids` and if available, the updated version is installed
    # e.g. CDSL.setup(["MW"], update=True)

Search in a dictionary::

    # Any loaded dictionary will be accessible like an attribute
    # e.g. CDSL.MW, CDSL.MWE etc.
    results = CDSL.MW.search("राम")

Access an entry by ID::

    entry = CDSL.MW.entry('263938')

    # >>> entry
    # <MWEntry: 263938: हृषीकेश = lord of the senses (said of Manas), BhP.>

Transliterate a single entry::

    # >>> entry.transliterate('slp1')
    # <MWEntry: 263938: hfzIkeSa = lord of the senses (said of Manas), BhP.>

Change transliteration scheme for a dictionary::

    CDSL.MW.set_scheme("itrans")
    CDSL.MW.search("rAma")


For a more detailed usage, check the documentation of modules in the PyCDSL Package.

https://pycdsl.readthedocs.io/en/latest/pycdsl.html


Using REPL Interface of PyCDSL
==============================

To use REPL Interface to Cologne Digital Sanskrit Lexicon (CDSL)::

    $ cdsl


Example of a REPL Session::

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
