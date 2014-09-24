"""
This package provides a text generator class and some utility functions that
can simply return the text you desire. There are 2 sets of functions:

* Those with **generate_** prefix that return the desired text and some stats
* Those with **get_** that return the desired text without the stats

On the average, you probably want to import the **get_** prefixed functions and
just get the text:

>>> from loremipsum import get_sentences
>>>
>>> sentences_list = get_sentences(5)
>>> len(sentences_list)
5
>>>

If you fancy some statistics, you want to import the **generate_**
prefixed functions:

>>> from loremipsum import generate_paragraph
>>>
>>> sentences_count, words_count, paragraph = generate_paragraph()

If you need generate text based on your own sample text and/or dictionary, you
want to import the **Generator** class:

>>> from loremipsum import Generator
>>>
>>> with open('data/sample.txt', 'r') as sample_txt
>>>     sample = sample_txt.read()
>>> with open('data/dictionary.txt', 'r') as dictionary_txt
>>>     dictionary = dictionary_txt.read().split()
>>>
>>> g = Generator(sample, dictionary)
>>> sentence = g.get_sentence()
>>>
"""

from functions import generate_paragraph
from functions import generate_paragraphs
from functions import generate_sentence
from functions import generate_sentences
from functions import get_paragraph
from functions import get_paragraphs
from functions import get_sentence
from functions import get_sentences
from functions import get_word
from functions import get_words
from generator import Generator

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
