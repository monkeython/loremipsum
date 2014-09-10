"""
A Lorem Ipsum text generator
============================

You can access this documenation on the interactive python2 shell like this:

>>> import loremipsum
>>> print loremipsum.__doc__

or with python3:

>>> import loremipsum
>>> print(loremipsum.__doc__)

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

# The following (not so) special variables have been created for sphinx
# conf.py and for setup.py
__author__ = "Luca De Vitis <luca@monkeython.com>"
__version__ = '1.0.3'
__copyright__ = "2011-2014, %s " % __author__
__license__ = """
   Copyright (C) %s

      This program is free software: you can redistribute it and/or modify
      it under the terms of the GNU General Public License as published by
      the Free Software Foundation, either version 3 of the License, or
      (at your option) any later version.

      This program is distributed in the hope that it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
      GNU General Public License for more details.

      You should have received a copy of the GNU General Public License
      along with this program.  If not, see <http://www.gnu.org/licenses/>
""" % __copyright__

__doc__ = """
:version: %s
:author: %s
:contact: http://www.monkeython.com
:copyright: %s

%s
""" % (__version__, __author__, __license__, __doc__)
__docformat__ = 'restructuredtext en'
__keywords__ = ['lorem', 'ipsum', 'text', 'generator']
__classifiers__ = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries :: Python Modules']

from .generator import Generator, DictionaryError, SampleError

__all__ = [
    'generate_sentence',
    'generate_sentences',
    'generate_paragraph',
    'generate_paragraphs',
    'get_sentence',
    'get_sentences',
    'get_paragraph',
    'get_paragraphs',
    'Generator',
    'DictionaryError',
    'SampleError']

_GENERATOR = Generator()


def generate_sentence(start_with_lorem=False):
    """
    Utility function to generate a single random sentence with stats.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :type start_with_lorem: bool
    :returns: a tuple with amount of sentences, words and the text
    :rtype: tuple(int, int, str)
    """
    return _GENERATOR.generate_sentence(start_with_lorem)


def generate_sentences(amount, start_with_lorem=False):
    """
    Generator function that yields specified amount of random sentences with
    stats.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :param amount: amount of sentences to generate.
    :type amount: int
    :returns: a tuple with amount of sentences, words and the text
    :rtype: tuple(int, int, str)
    """
    return _GENERATOR.generate_sentences(amount, start_with_lorem)


def generate_paragraph(start_with_lorem=False):
    """
    Utility function to generate a single random paragraph with stats.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :returns: a tuple with amount of sentences, words and the text
    :rtype: tuple(int, int, str)
    """
    return _GENERATOR.generate_paragraph(start_with_lorem)


def generate_paragraphs(amount, start_with_lorem=False):
    """
    Generator function that yields specified amount of random paragraphs with
    stats.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :returns: a tuple with amount of sentences, words and the text
    :rtype: tuple(int, int, str)
    """
    return _GENERATOR.generate_paragraphs(amount, start_with_lorem)


def get_sentence(start_with_lorem=False):
    """
    Utility function to get a single random sentence.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :returns: a random sentence
    :rtype: str
    """
    return _GENERATOR.generate_sentence(start_with_lorem)[-1]


def get_sentences(amount, start_with_lorem=False):
    """
    Utility function to get specified amount of random sentences.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :param amount: amount of sentences to get.
    :type amount: int
    :returns: a list of random sentences.
    :rtype: list
    """
    sentences = _GENERATOR.generate_sentences(amount, start_with_lorem)
    return [s[-1] for s in sentences]


def get_paragraph(start_with_lorem=False):
    """
    Utility function to get a single random paragraph.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :returns: a random paragrpah
    :rtype: str
    """
    return _GENERATOR.generate_paragraph(start_with_lorem)[-1]


def get_paragraphs(amount, start_with_lorem=False):
    """
    Utility function to get specified amount of random paragraphs.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :returns: a list of random paragraphs
    :rtype: list
    """
    paragraphs = _GENERATOR.generate_paragraphs(amount, start_with_lorem)
    return [p[-1] for p in paragraphs]
