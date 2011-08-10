"""
This module provide a simple way to generate "Lorem Ipsum" paragraphs,
sentences, or just random words.
"""
import math
from random import normalvariate, choice
import re
from pkg_resources import resource_string

__author__ = "Luca De Vitis <luca@monkeython.com>"
__version__ = '0.1'
__copyright__ = "2011, %s " % __author__
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
:abstract: %s
:version: %s
:author: %s
:organization: Monkeython
:contact: http://www.monkeython.com
:copyright: %s
""" % (' '.join(__doc__.splitlines()), __version__, __author__, __license__)
__docformat__ = 'restructuredtext en'
__classifiers__ = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Topic :: Internet :: WWW/HTTP' ]

# Delimiters that mark ends of sentences
_SENTENCES_DELIMITERS = ['.', '?', '!']

# Delimiters which do not form parts of words (i.e. "hello," is the word
# "hello" with a comma next to it)
_WORDS_DELIMITERS = [','] + _SENTENCES_DELIMITERS

_SAMPLE = resource_string('loremipsum', 'data/sample.txt')
_DICTIONARY = resource_string('loremipsum', 'data/dictionary.txt').split()

_LOREM_IPSUM = "lorem ipsum dolor sit amet, consecteteur adipiscing elit"

def _paragraphs(text):
    """
    Splits a piece of text into paragraphs, separated by empty lines.
    """
    paragraphs = [[]]
    for line in text.splitlines():
        if line.strip():
            paragraphs[-1].append(line)
        elif paragraphs[-1]:
            paragraphs.append([])
    return filter(None, [' '.join(p).strip() for p in paragraphs])

def _sentences(text):
    """
    Splits a piece of text into sentences, separated by periods, question 
    marks and exclamation marks.
    """
    delimiters = '[%s]' % ''.join(['\\' + d for d in _SENTENCES_DELIMITERS])
    sentences = re.split(delimiters, text.strip())
    return filter(None, [s.strip() for s in sentences])

def _mean(values):
    """
    Calculate the mean for a list of integers.
    """
    return sum(values) / float(max(len(values), 1))

def _variance(values):
    """
    Calculate the variance for a list of integers.
    """
    return _mean([v**2 for v in values]) - _mean(values)**2

def _sigma(values):
    """
    Calculate the sigma for a list of integers.
    """
    return math.sqrt(_variance(values))

class DictionaryError(Exception):
    """
    The dictionary must be a list of one or more words.
    """
    def __str__(self):
        return self.__doc__

class SampleError(Exception):
    """
    The sample text must contain one or more empty-line delimited paragraphs,
    and each paragraph must contain one or more period, question mark, or
    exclamation mark delimited sentences.
    """
    def __str__(self):
        return self.__doc__

class Generator(object):
    """
    Generates random strings of "lorem ipsum" text.

    Markov chains are used to generate the random text based on the analysis 
    of a sample text. In the analysis, only paragraph, sentence and word 
    lengths, and some basic punctuation matter -- the actual words are 
    ignored. A provided list of words is then used to generate the random text,
    so that it will have a similar distribution of paragraph, sentence and word
    lengths.

    :param sample: a string containing the sample text
    :type sample: str
    :param dictionary: a string containing a list of words
    :type dictionary: list
    """

    # Words that can be used in the generated output
    # Maps a word-length to a list of words of that length
    __dictionary = {}

    # Chains of three words that appear in the sample text
    # Maps a pair of word-lengths to a third word-length and an optional 
    # piece of trailing punctuation (for example, a period, comma, etc.)
    __chains = {}

    # Pairs of word-lengths that can appear at the beginning of sentences
    __starts = []

    # Sample that the generated text is based on
    __sample = ""

    # Statistics for sentence and paragraph generation
    __sentence_mean = 0
    __sentence_sigma = 0
    __paragraph_mean = 0
    __paragraph_sigma = 0

    # Last calculated statistics, in case they are overwritten by user
    __generated_sentence_mean = 0
    __generated_sentence_sigma = 0
    __generated_paragraph_mean = 0
    __generated_paragraph_sigma = 0

    def __init__(self, sample=None, dictionary=None):
        self.sample = sample or _SAMPLE
        self.dictionary = dictionary or _DICTIONARY

    def __get_sentence_mean(self):
        """
        A non-negative value determining the mean sentence length (in words)
        of generated sentences. Is changed to match the sample text when the
        sample text is updated.

        :rtype: int
        :raises: :py:exc:`ValueError` if value is lesser then 0
        """
        return self.__sentence_mean

    def __set_sentence_mean(self, mean):
        if mean < 0:
            raise ValueError('Mean sentence length must be non-negative.')
        self.__sentence_mean = mean

    sentence_mean = property(__get_sentence_mean, __set_sentence_mean)

    def __get_sentence_sigma(self):
        """
        A non-negative value determining the standard deviation of sentence
        lengths (in words) of generated sentences. Is changed to match the
        sample text when the sample text is updated.

        :rtype: int
        :raises: :py:exc:`ValueError` if value is lesser then 0
        """
        return self.__sentence_sigma

    def __set_sentence_sigma(self, sigma):
        if sigma < 0:
            raise ValueError('Standard deviation of sentence length must be '
                'non-negative.')
        self.__sentence_sigma = sigma

    sentence_sigma = property(__get_sentence_sigma, __set_sentence_sigma)

    def __get_paragraph_mean(self):
        """
        A non-negative value determining the mean paragraph length (in
        sentences) of generated sentences. Is changed to match the sample text
        when the sample text is updated.

        :rtype: int
        :raises: :py:exc:`ValueError` if value is lesser then 0
        """
        return self.__paragraph_mean

    def __set_paragraph_mean(self, mean):
        if mean < 0:
            raise ValueError('Mean paragraph length must be non-negative.')
        self.__paragraph_mean = mean

    paragraph_mean = property(__get_paragraph_mean, __set_paragraph_mean)

    def __get_paragraph_sigma(self):
        """
        A non-negative value determining the standard deviation of paragraph
        lengths (in sentences) of generated sentences. Is changed to match the
        sample text when the sample text is updated.

        :rtype: int
        :raises: :py:exc:`ValueError` if value is lesser then 0
        """
        return self.__paragraph_sigma

    def __set_paragraph_sigma(self, sigma):
        if sigma < 0:
            raise ValueError('Standard deviation of paragraph length must be '
                'non-negative.')
        self.__paragraph_sigma = sigma

    paragraph_sigma = property(__get_paragraph_sigma, __set_paragraph_sigma)

    def reset_statistics(self):
        """
        Returns the values of :py:attr:`sentence_mean`,
        :py:attr:`sentence_sigma`, :py:attr:`paragraph_mean`, and
        :py:attr:`paragraph_sigma` to their values as calculated from the
        sample text.
        """
        self.sentence_mean = self.__generated_sentence_mean
        self.sentence_sigma = self.__generated_sentence_sigma
        self.paragraph_mean = self.__generated_paragraph_mean
        self.paragraph_sigma = self.__generated_paragraph_sigma

    def __get_sample(self):
        """
        The sample text that generated sentences are based on.

        Sentences are generated so that they will have a similar distribution 
        of word, sentence and paragraph lengths and punctuation.

        Sample text should be a string consisting of a number of paragraphs, 
        each separated by empty lines. Each paragraph should consist of a 
        number of sentences, separated by periods, exclamation marks and/or
        question marks. Sentences consist of words, separated by white space.

        :param sample: the sample text
        :type sample: str
        :rtype: str
        :raises: :py:exc:`SampleError` if no words in sample text
        """
        return self.__sample

    def __set_sample(self, sample):
        words = sample.split()
        previous = (0, 0)
        chains = {}
        starts = [previous]

        # Generates the __chains and __starts values required for sentence
        # generation.
        for word in words:
            length, delimiter = len(word), ''
            for d in _WORDS_DELIMITERS:
                if word.endswith(d):
                    length, delimiter = length -1, delimiter
                    break
            if length > 0:
                chains.setdefault(previous, []).append((length, delimiter))
                if delimiter:
                    starts.append(previous)
                previous = (previous[1], length)
        if chains:
            self.__sample = sample
            self.__chains = chains
            self.__starts = starts

            # Calculates the mean and standard deviation of the lengths of
            # sentences (in words) in a sample text.
            sentences = filter(None, [s.strip() for s in _sentences(sample)])
            sentences_lengths = [len(s.split()) for s in sentences ]
            self.__generated_sentence_mean = _mean(sentences_lengths)
            self.__generated_sentence_sigma = _sigma(sentences_lengths)

            # Calculates the mean and standard deviation of the lengths of
            # paragraphs (in sentences) in a sample text.
            paragraphs = filter(None, [p.strip() for p in _paragraphs(sample)])
            paragraphs_lengths = [len(_sentences(p)) for p in paragraphs]
            self.__generated_paragraph_mean = _mean(paragraphs_lengths)
            self.__generated_paragraph_sigma = _sigma(paragraphs_lengths)

            self.reset_statistics()
        else:
            raise SampleError

    sample = property(__get_sample, __set_sample)

    def __get_dictionary(self):
        """
        A dictionary of words that generated sentences are made of, grouped by
        words length.

        :param words: list of words
        :type words: list
        :rtype: dict
        :raises: :py:exc:`DictionaryError` if no valid words in dictionary
        """
        return self.__dictionary.copy()

    def __set_dictionary(self, words):
        self.__dictionary = dict()
        self.__words = list()
        for word in words:
            try:
                word = str(word)
            except TypeError:
                continue
            else:
                self.__dictionary.setdefault(len(word), set()).add(word)
                self.__words.append(word)

        if not (self.__dictionary and self.__words):
            raise DictionaryError

    dictionary = property(__get_dictionary, __set_dictionary)

    @property
    def words(self):
        """
        The plain list of words in the dictionary.
        """
        return self.__words[:]

    def generate_sentence(self, start_with_lorem=False):
        """
        Generates a single sentence, of random length.

        :param start_with_lorem: if True, then the text will begin with the
                                 standard "Lorem ipsum..." first sentence.
        :type start_with_lorem: bool
        """

        # The length of the sentence is a normally distributed random variable.
        mean, sigma = self.sentence_mean, self.sentence_sigma
        sentence_length = max(2, int(round(normalvariate(mean, sigma))))

        words = []
        previous = ()
        last_word = ''

        word_delimiter = '' # Defined here in case while loop doesn't run

        # Start the sentence with "Lorem ipsum...", if desired
        if start_with_lorem:
            words.extend(_LOREM_IPSUM.split()[:sentence_length])
            last_char = words[-1][-1]
            if last_char in _WORDS_DELIMITERS:
                word_delimiter = last_char

        # Generate a sentence from the "chains"
        for w in xrange(sentence_length - len(words)):
            # If the current starting point is invalid, choose another randomly
            if (not self.__chains.has_key(previous)):
                starts = set(self.__starts)
                chains = set(self.__chains.keys())
                previous = choice(list(chains.intersection(starts)))

            # Choose the next "chain" to go to. This determines the next word
            # length we'll use, and whether there is e.g. a comma at the end of
            # the word.
            chain = choice(self.__chains[previous])
            word_length = chain[0]

            # If the word delimiter contained in the chain is also a sentence
            # delimiter, then we don't include it because we don't want the
            # sentence to end prematurely (we want the length to match the
            # sentence_length value).
            if chain[1] in _SENTENCES_DELIMITERS:
                word_delimiter = ''
            else:
                word_delimiter = chain[1]

            # Choose a word randomly that matches (or closely matches) the
            # length we're after.
            lengths = self.__dictionary.keys()
            closest = lengths[0]
            for length in lengths:
                if abs(word_length - length) < abs(word_length - closest):
                    closest = length

            # Readability. No word can appear next to itself.
            word = choice(list(self.__dictionary[closest]))
            while word == last_word:
                word = choice(list(self.__dictionary[closest]))
            last_word = word

            words.append(word + word_delimiter)
            previous = (previous[1], word_length)

        # Finish the sentence off with capitalisation, a period and
        # form it into a string
        sentence = ' '.join(words).capitalize().rstrip(word_delimiter) + '.'
        return (1, len(words), sentence)

    def generate_sentences(self, amount, start_with_lorem=False):
        """
        Generator method that yields sentences, of random length.

        :param start_with_lorem: if True, then the text will begin with the
                                 standard "Lorem ipsum..." first sentence.
        :type start_with_lorem: bool
        """
        yield self.generate_sentence(start_with_lorem)
        for s in xrange(amount - 1):
            yield self.generate_sentence()

    def generate_paragraph(self, start_with_lorem=False):
        """
        Generates a single lorem ipsum paragraph, of random length.

        :param start_with_lorem: if True, then the text will begin with the
                                 standard "Lorem ipsum..." first sentence.
        :type start_with_lorem: bool
        """

        # The length of the paragraph is a normally distributed random variable.
        mean, sigma = self.paragraph_mean, self.paragraph_sigma
        sentences = max(2, int(round(normalvariate(mean, sigma))))

        words = 0
        paragraph = []
        generate = self.generate_sentences
        for void, word_count, sentence in generate(sentences, start_with_lorem):
            words += word_count
            paragraph.append(sentence)

        # Form the paragraph into a string.
        return (sentences, words, ' '.join(paragraph))

    def generate_paragraphs(self, amount, start_with_lorem=False):
        """
        Generator method that yields paragraphs, of random length.

        :param start_with_lorem: if True, then the text will begin with the
                                 standard "Lorem ipsum..." first sentence.
        :type start_with_lorem: bool
        """
        yield self.generate_paragraph(start_with_lorem)
        for p in xrange(amount - 1):
            yield self.generate_paragraph()

_generator = Generator()

def generate_sentence(start_with_lorem=False):
    """
    Utility function to generate a single random sentence with stats.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :type start_with_lorem: bool
    :returns: a tuple with amount of sentences, words and the text
    :rtype: tuple(int, int, str)
    """
    return _generator.generate_sentence(start_with_lorem)

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
    return _generator.generate_sentences(amount, start_with_lorem)

def generate_paragraph(start_with_lorem=False):
    """
    Utility function to generate a single random paragraph with stats.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :returns: a tuple with amount of sentences, words and the text
    :rtype: tuple(int, int, str)
    """
    return _generator.generate_paragraph(start_with_lorem)

def generate_paragraphs(amount, start_with_lorem=False):
    """
    Generator function that yields specified amount of random paragraphs with
    stats.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :returns: a tuple with amount of sentences, words and the text
    :rtype: tuple(int, int, str)
    """
    return _generator.generate_paragraphs(amount, start_with_lorem)

def get_sentence(start_with_lorem=False):
    """
    Utility function to get a single random sentence.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :returns: a random sentence
    :rtype: str
    """
    return _generator.generate_sentence(start_with_lorem)[-1]

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
    sentences = _generator.generate_sentences(amount, start_with_lorem)
    return [s[-1] for s in sentences]

def get_paragraph(start_with_lorem=False):
    """
    Utility function to get a single random paragraph.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :returns: a random paragrpah
    :rtype: str
    """
    return _generator.generate_paragraph(start_with_lorem)[-1]

def get_paragraphs(amount, start_with_lorem=False):
    """
    Utility function to get specified amount of random paragraphs.

    :param start_with_lorem: if True, then the text will begin with the
                             standard "Lorem ipsum..." first sentence.
    :returns: a list of random paragraphs
    :rtype: list
    """
    paragraphs = _generator.generate_paragraphs(amount, start_with_lorem)
    return [p[-1] for p in paragraphs]

