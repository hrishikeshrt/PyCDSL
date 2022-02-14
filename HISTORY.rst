History
=======

0.6.0 (2022-02-14)
------------------

* Add :code:`__getitem__` method to :code:`CDSLCorpus` to access loaded dictionaries using `[]` operator with :code:`dict_id`
* Add :code:`__getitem__` method to :code:`CDSLDict` to access dictionary entries using `[]` operator with :code:`entry_id`
* Add unit tests and integration tests for :code:`pycdsl.utils`
* Add unit tests and integration tests for :code:`pycdsl.corpus`
* Update documentation
* Fix bugs

0.5.0 (2022-02-13)
------------------

* Add :code:`model_map` argument to :code:`CDSLDict.connect` for better customization
* Make :code:`CDSLCorpus` iterable (iterate over loaded dictionaries)
* Make :code:`CDSLDict` iterable (iterate over dictionary entries)
* Update documentation

0.4.0 (2022-02-12)
------------------

* Add ability to limit and offset the number of search results
* Add :code:`.to_dict()` method to :code:`Entry` class
* Add multi-dictionary :code:`.search()` from :code:`CDSLCorpus`
* Add support for multiple active dictionaries in REPL
* Improve code structure (more modular)
* Improve documentation formatting
* Update documentation
* Fix bugs

0.3.0 (2022-02-07)
------------------

* Functional CLI (console command) for dictionary search
* Integration of existing REPL into the CLI. (:code:`--interactive`)
* Extend transliteration support on Corpus, Dictionary, Search and Entry level
* Make the package Python 3.6 compatibile

0.2.0 (2022-02-05)
------------------

* Improve dictionary setup
* Add a function to dump data
* Add logging support
* Add transliteration support using :code:`indic-transliteration`

0.1.0 (2022-01-28)
------------------

* First release on PyPI.
