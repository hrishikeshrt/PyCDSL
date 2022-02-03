======
PyCDSL
======


.. image:: https://img.shields.io/pypi/v/PyCDSL?color=success
        :target: https://pypi.python.org/pypi/PyCDSL

.. image:: https://img.shields.io/travis/hrishikeshrt/pycdsl.svg
        :target: https://travis-ci.com/hrishikeshrt/pycdsl

.. image:: https://readthedocs.org/projects/pycdsl/badge/?version=latest
        :target: https://pycdsl.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



PyCDSL is a python interface to Cologne Digital Sanskrit Lexicon (CDSL)
https://www.sanskrit-lexicon.uni-koeln.de/

It lets you download and access various dictionaries from CDSL
programmatically as well as through a REPL.


* Free software: GNU General Public License v3
* Documentation: https://pycdsl.readthedocs.io.


Features
--------

* CDSL Corpus Management (Download, Update, Access)
* Unified Programmable Interface to access all dictionaries available at CDSL
* REPL Interface for easy dictionary search


Usage
-----

PyCDSL can be used in a project for programmatic access as well as from the shell
as a REPL interface.

Using PyCDSL in a Project
^^^^^^^^^^^^^^^^^^^^^^^^^

To use PyCDSL in a project::

    import pycdsl

Create a CDSLCorpus Instance::

    # Default installation at ~/cdsl_data
    # Custom installation path can be pased to the instantiation
    CDSL = pycdsl.CDSLCorpus()

Setup default dictionaries (MW, MWE, AP90, AE)::

    # If any additional dictionaries are installed, they will be loaded as well
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


Using REPL Interface of PyCDSL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use REPL Interface to Cologne Digital Sanskrit Lexicon (CDSL)::

    $ cdsl

Example of a :code:`cdsl` REPL Session::

    Cologne Sanskrit Digital Lexicon (CDSL)
    ---------------------------------------
    Install or load a lexicon by typing `use <DICT_ID>` e.g. `use MW`.
    Type any keyword to search in the selected lexicon. (help or ? for list of options)
    Loaded 4 dictionaries.

    (CDSL::None) help

    Documented commands (type help <topic>):
    ========================================
    EOF        debug  exit  info    shell  update  version
    available  dicts  help  scheme  show   use

    (CDSL::None) help available
    Display lexicons available in CDSL

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

    (CDSL::MW) scheme itrans

    Input scheme: itrans

    (CDSL::MW) hRRiSIkesha

    <MWEntry: 263922: हृषीकेश = हृषी-केश a   See below under हृषीक.>
    <MWEntry: 263934: हृषीकेश = हृषीकेश b m. (perhaps = हृषी-केश cf. हृषी-वत् above) id. (-त्व n.), MBh.; Hariv. &c.>
    <MWEntry: 263935: हृषीकेश = N. of the tenth month, VarBṛS.>
    <MWEntry: 263936: हृषीकेश = of a Tīrtha, Cat.>
    <MWEntry: 263937: हृषीकेश = of a poet, ib.>
    <MWEntry: 263938: हृषीकेश = lord of the senses (said of Manas), BhP.>

    (CDSL::MW) info

    CDSLDict(id='MW', date='1899', name='Monier-Williams Sanskrit-English Dictionary')

    (CDSL::MW) exit

    Bye


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
