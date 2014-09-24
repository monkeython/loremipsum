"""
This module provides a set of functions to easily interface with a
:py:class:`loremipsum.generator.Generator` instance loaded with famous "Lorem
ipsum" pseudo latin text.
"""

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
    'get_paragraphs']

from loremipsum import generator

import pkg_resources as pkg

# Delimiters that mark ends of sentences
_SENTENCE_DELIMITERS = ('.', '?', '!')

# Delimiters which do not form parts of words (i.e. "hello," is the word
# "hello" with a comma next to it)
_WORD_DELIMITERS = (',',) + _SENTENCE_DELIMITERS

# Sample lorem ipsum text.
_SAMPLE = pkg.resource_string(__name__, 'default/sample.txt').decode('utf-8')

# Pseudo-latin lexicon.
_LEXICON = pkg.resource_string(__name__, 'default/lexicon.txt').decode('utf-8')

_LOREMIPSUM = generator.Generator(_SAMPLE,
                                  _LEXICON.splitlines(),
                                  _WORD_DELIMITERS,
                                  _SENTENCE_DELIMITERS)


def generate_sentence(**args):
    """Create a single plausible latin sentence, with stats.

    The created sentence is returned along with the amount of words used. This
    function accepts the same arguments and returns the same as
    :py:meth:`Generator.generate_sentence`.
    """
    return _LOREMIPSUM.generate_sentence(**args)


def generate_sentences(amount, **args):
    """Creates a generator of plausible latin sentences, with stats.

    The generator will produce the specified amount of sentences with stats.
    This function accepts the same arguments and returns the same as
    as :py:meth:`Generator.generate_sentences`.
    """
    return _LOREMIPSUM.generate_sentences(amount, **args)


def generate_paragraph(**args):
    """Create a single plausible latin paragraph, with stats.

    The generated text is a single line paragraph and is returned along with
    the amount of sentences and words used. This function accepts the same
    arguments and returns the same as as
    :py:meth:`Generator.generate_paragraph`.
    """
    return _LOREMIPSUM.generate_paragraph(**args)


def generate_paragraphs(amount, **args):
    """Creates a generator of plausible latin paragraphs, with stats.

    The generator will produce the specified amount of paragraphs with stats.
    This function accepts the same arguments and returns the same as as
    :py:meth:`Generator.generate_paragraphs`.
    """
    return _LOREMIPSUM.generate_paragraphs(amount, **args)


def get_word(length=None):
    """Selects a random word from the from the loremipsum sample lexicon.

    This function accepts the same arguments and returns the same as
    :py:meth:`Generator.generate_word`.
    """
    return _LOREMIPSUM.generate_word(length)


def get_words(amount, length=None):
    """Creates a generatator of the specified amount of words.

    This function accepts the same arguments and returns the same as
    :py:meth:`Generator.generate_words`.
    """
    return _LOREMIPSUM.generate_words(amount, length)


def get_sentence(**args):
    """Creates a single plausible latin sentence.

    This function accepts the same arguments as
    :py:meth:`Generator.generate_sentence`.

    :rtype: str or unicode
    """
    return generate_sentence(**args)[-1]


def get_sentences(amount, **args):
    """Creates a list of plausible latin sentences.

    The list contains just the sentences. This function accepts the same
    arguments as :py:meth:`Generator.generate_sentences`.

    :rtype: list(str or unicode, ...)
    """
    return [s[-1] for s in generate_sentences(amount, **args)]


def get_paragraph(**args):
    """Creates a single plausible latin paragraph.

    This function accepts the same arguments as
    :py:meth:`Generator.generate_paragraph`.

    :rtype: str or unicode
    """
    return generate_paragraph(**args)[-1]


def get_paragraphs(amount, **args):
    """Creates a list of plausible latin paragraphs.

    The list contains just the paragraphs text. This function accepts the same
    arguments as :py:meth:`Generator.generate_paragraph`.

    :rtype: list(str or unicode, ...)
    """
    return [p[-1] for p in generate_paragraphs(amount, **args)]
