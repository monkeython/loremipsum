"""
This package provides a text generator class and some utility functions that
can simply return the text you desire. There are 2 sets of functions:

* Those with **generate_** prefix that return the desired text and some stats
* Those with **get_** that return the desired text without the stats

On the average, you probably want to import the **get_** prefixed functions and
just get the text:

>>> import loremipsum
>>>
>>> loremipsum.sentences_list = get_sentences(5)
>>> len(sentences_list)
5
>>>

If you fancy some statistics, you want to import the **generate_**
prefixed functions:

>>> import loremipsum
>>>
>>> sentences_count, words_count, paragraph = loremipsum.generate_paragraph()

If you need generate text based on your own sample text and/or dictionary, you
want to import the **Generator** class:

>>> import loremipsum
>>>
>>> with open('data/sample.txt', 'r') as sample_txt
>>>     sample = sample_txt.read()
>>> with open('data/lexicon.txt', 'r') as lexicon_txt
>>>     dictionary = lexicon_txt.read().split()
>>>
>>> sentence_delimiters = ('.', '?', '!')
>>> word_relimiters = (',',) + sentence_delimiters
>>> g = loremipsum.Generator(sample, dictionary,
                             word_relimiters, sentence_delimiters)
>>> sentence = g.get_sentence()
>>>
"""

__author__ = "Luca De Vitis <luca@monkeython.com>"
__version__ = '2.0.0-b1'
__copyright__ = "2014, %s " % __author__
__docformat__ = 'restructuredtext en'
__keywords__ = ['lorem', 'ipsum', 'text', 'generator']
# 'Development Status :: 5 - Production/Stable',
__classifiers__ = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: Jython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules']

from loremipsum import functions
from loremipsum import generator

generate_paragraph = functions.generate_paragraph
generate_paragraphs = functions.generate_paragraphs
generate_sentence = functions.generate_sentence
generate_sentences = functions.generate_sentences
get_paragraph = functions.get_paragraph
get_paragraphs = functions.get_paragraphs
get_sentence = functions.get_sentence
get_sentences = functions.get_sentences
get_word = functions.get_word
get_words = functions.get_words
Generator = generator.Generator

__all__ = [
    'generate_sentence',
    'generate_sentences',
    'generate_paragraph',
    'generate_paragraphs',
    'get_word',
    'get_words',
    'get_sentence',
    'get_sentences',
    'get_paragraph',
    'get_paragraphs',
    'Generator']
