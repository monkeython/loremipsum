"""
"""

from loremipsum import generator

import pkg_resources

sample = pkg_resources.resource_string(
    __name__, 'loremipsum/sample.txt').decode('utf-8')
lexicon = pkg_resources.resource_string(
    __name__, 'loremipsum/lexicon.txt').decode('utf-8')
word_delimiters = pkg_resources.resource_string(
    __name__, 'loremipsum/word_delimiters.txt').decode('utf-8')
sentence_delimiters = pkg_resources.resource_string(
    __name__, 'loremipsum/sentence_delimiters.txt').decode('utf-8')
loremipsum = generator.Sample(text=sample,
                              lexicon=lexicon,
                              word_delimiters=word_delimiters,
                              sentence_delimiters=sentence_delimiters)

__all__ = ['loremipsum']
