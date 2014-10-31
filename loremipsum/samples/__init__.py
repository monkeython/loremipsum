"""
This package provides a collection of sample to be used by
:py:class:`loremipsum.generator.Generator`

Default sample is named ``loremipsum``. This is a pluggable package.
"""

from loremipsum import generator

import pkg_resources

_resource = lambda n: pkg_resources.resource_string(__name__, n).decode('UTF-8')

_text = resource('loremipsum/sample.txt')
_lexicon = resource('loremipsum/lexicon.txt')
_word_delimiters = resource('loremipsum/word_delimiters.txt')
_sentence_delimiters = resource('loremipsum/sentence_delimiters.txt')

loremipsum = generator.Sample(text=_text,
                              lexicon=_lexicon,
                              word_delimiters=_word_delimiters,
                              sentence_delimiters=_sentence_delimiters)

__all__ = ['loremipsum']
