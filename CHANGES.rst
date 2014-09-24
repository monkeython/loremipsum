Changes
=======

2.0.0-b1
   * New API for the **Generator** class: now takes all the needed params from
     the constructor and no default value is implied. Unlike the previous
     version, now also wants a list of delimiters for the words and one for the
     sentences.
   * No more custom exceptions. Now **Generator** class uses python standard
     **ValueError** if the values used in the constructor are wrong.
   * No more property setters: Now **Generator** objects are "Read-Only".
   * New property **incipit** which returns the first sample sentence.
   * New API for the **Generator.generate_** methods: now developers can
     override sentences and paragraphs mean and sigma values, as well as fixing
     their lienght.
   * New **Generator** methods to generate siply words: generate_word and generate_words
   * New **loremipsum** functions API to reflects the new **Generator** API.
   * New **loremipsum** functions to interface with new **Generator** methods: get_word and get_words
1.0.5
   * Added python3 support: fixes #8
   * Added README.rst to MANIFEST.in: fixes #9
1.0.4
   * Added MANIFEST.in
   * Removed dependencies on distribute
   * Applied pep8 and pylint suggested cleanup
1.0.3
   * Fix issue #5
1.0.2
   * Now is a package: fixes datafiles distribution.
1.0.1
   * Added support for python 2.5
1.0.0
   * Added unittests.
   * Added documentation.
   * Added stats to text generators methods in **Generator**
   * Added generator methods in **Generator**, for multiple text generations
   * Added stats-less text generators fuctions to module
    
0.1.0
   * First release.
