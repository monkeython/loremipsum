"""
This module provides a set of functions to easily interface with a
:py:class:`loremipsum.generator.Generator` instance loaded with famous "Lorem
ipsum" pseudo latin text.
"""

__all__ = [
    'get_word',
    'get_words',
    'get_sentence',
    'get_sentences',
    'get_paragraph',
    'get_paragraphs',
    'generate_sentence',
    'generate_sentences',
    'generate_paragraph',
    'generate_paragraphs']

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


def get_word(length=None):
    """Selects a random word from the from the loremipsum sample lexicon.

    This function accepts the same arguments and returns the same as
    :py:meth:`Generator.generate_word`.

    :rtype: str or unicode

    >>> import loremipsum
    >>>
    >>> # Just get a word
    >>> loremipsum.get_word()
    u'neque'
    >>>
    >>> # Get a 6 charaters long word
    >>> loremipsum.get_word(6)
    u'turpis'
    """
    return _LOREMIPSUM.generate_word(length)


def get_words(amount, length=None):
    """Creates a generatator of the specified amount of words.

    This function accepts the same arguments and returns the same as
    :py:meth:`Generator.generate_words`.

    :rtype: generator

    >>> import loremipsum
    >>>
    >>> # Just get 3 words
    >>> list(loremipsum.get_words(3))
    [u'lorem', u'fringilla', u'class']
    >>>
    >>> # Get 4 words which are 5 charaters long
    >>> list(loremipsum.get_words(4,5))
    [u'justo', u'curae', u'morbi', u'porta']
    """
    return _LOREMIPSUM.generate_words(amount, length)


def get_sentence(**args):
    """Creates a single plausible latin sentence.

    This function accepts the same arguments as
    :py:meth:`Generator.generate_sentence`.

    :rtype: str or unicode

    >>> import loremipsum
    >>>
    >>> # Just get a sentence
    >>> loremipsum.get_sentence()
    u'Laoreet nulla sed donec dis magna nisi mauris, aliquam urna donec vel.'
    >>>
    >>> # You can make it startss with famous 'Lorem ipsum incipit
    >>> loremipsum.get_sentence(incipit=True)
    u'Lorem ipsum dolor sit.'
    >>>
    >>> # Or you can force its length
    >>> loremipsum.get_sentence(sentence_len=5)
    u'Praesent vulputate massa porta nullam.'
    """
    return _LOREMIPSUM.generate_sentence(**args)[-1]


def get_sentences(amount, **args):
    """Creates a generator of plausible latin sentences.

    The generator yields just the sentences. This function accepts the same
    arguments as :py:meth:`Generator.generate_sentences`.

    :rtype: generator

    >>> from __future__ import print_function
    >>> import loremipsum
    >>>
    >>> # Get a generator of sentence
    >>> for s in loremipsum.get_sentences(3):
    ...  print(s)
    ...
    Nisi pede erat justo tristique nascetur.
    Sodales, felis aliquet quisque porta urna magna.
    Risus proin montes velit felis non eget leo.
    >>>
    >>> # Should you ever need, you can adjust mean and sigma values to alter
    >>> # the random words count in a sentence. The following should generate
    >>> # rather shot sentences
    >>> sentences = loremipsum.get_sentences(10,
    ...                                      sentence_mean=0.9,
    ...                                      sentence_sigma=0.9)
    >>> for s in sentences:
    ...  print(s)
    ...
    Sem id.
    Nisl volutpat.
    Eni a tortor.
    Nulla, imperdiet pede sodales.
    Arcu dictum ve.
    Nisi elit.
    Ipsum rutrum.
    Eu, aptent eu.
    Nibh, etiam.
    Et orci in velit taciti.
    >>>
    >>> # If you'd like to get the famous incipit, only the first sentence will
    >>> # have it
    >>> sentences = loremipsum.get_sentences(5,
    ...                                      incipit=True,
    ...                                      sentence_mean=0.9,
    ...                                      sentence_sigma=0.9)
    >>> for s in sentences:
    ...  print(s)
    ...
    Lorem ipsum dolor.
    At, tempor potenti.
    Pellentesque quisque duis.
    Condimentum accumsan laoreet.
    Suscipit pede.
    """
    for sentence in _LOREMIPSUM.generate_sentences(amount, **args):
        yield sentence[-1]


def get_paragraph(**args):
    """Creates a single plausible latin paragraph.

    This function accepts the same arguments as
    :py:meth:`Generator.generate_paragraph`.

    :rtype: str or unicode

    >>> import loremipsum
    >>>
    >>> # You can just get a paragraph.
    >>> paragraph = loremipsum.get_paragraph()
    >>>
    >>> # Since default paragraph would be quite a long text...
    >>> loremipsum.get_paragraph(paragraph_mean=0.9,
    ...                          paragraph_sigma=0.9,
    ...                          sentence_mean=1.5,
    ...                          sentence_sigma=1.5)
    u'Ut quam. Netus ac. Commodo, porta risus conubia.'
    """
    return _LOREMIPSUM.generate_paragraph(**args)[-1]


def get_paragraphs(amount, **args):
    """Creates a generator of plausible latin paragraphs.

    The generator yields just the paragraphs text. This function accepts the
    same arguments as :py:meth:`Generator.generate_paragraph`.

    :rtype: generator

    >>> import loremipsum
    >>>
    >>> len('\n\n'.join(list(loremipsum.get_paragraphs(3))))
    2475
    """
    for paragraph in _LOREMIPSUM.generate_paragraphs(amount, **args):
        yield paragraph[-1]


def generate_sentence(**args):
    """Create a single plausible latin sentence, with stats.

    The created sentence is returned along with the amount of words used. This
    function accepts the same arguments and returns the same as
    :py:meth:`Generator.generate_sentence`.

    :rtype: tuple

    >>> import loremipsum
    >>>
    >>> # Just generate a sentence
    >>> loremipsum.generate_sentence()
    (8, u'Conubia euismod orci eros, suscipit tortor, magna tincidunt.')
    >>>
    >>> # You can make it startss with famous 'Lorem ipsum incipit
    >>> loremipsum.generate_sentence(incipit=True)
    (7, u'Lorem ipsum dolor sit amet, consectetuer adipiscing.')
    >>>
    >>> # Or you can force its length
    >>> loremipsum.generate_sentence(sentence_len=5)
    (5, u'Pede, nisl dolor nisl congue.')
    """
    return _LOREMIPSUM.generate_sentence(**args)


def generate_sentences(amount, **args):
    """Creates a generator of plausible latin sentences, with stats.

    The generator will produce the specified amount of sentences with stats.
    This function accepts the same arguments and returns the same as
    as :py:meth:`Generator.generate_sentences`.

    :rtype: generator

    >>> from __future__ import print_function
    >>> import loremipsum
    >>>
    >>> # Get a list of sentence
    >>> for s in loremipsum.generate_sentences(3):
    ...  print(s)
    ...
    (5, u'Pharetra, in, odio fermentum id.')
    (10, u'Amet fames dolor, aptent curae ad auctor dui congue, cum.')
    (9, u'Fames turpis curae morbi senectus dolor cum pede facilisis.')
    >>>
    >>> # Should you ever need, you can adjust mean and sigma values to alter
    >>> # the random words count in a sentence. The following should generate
    >>> # rather shot sentences
    >>> sentences = loremipsum.generate_sentences(6,
    ...                                           sentence_mean=0.9,
    ...                                           sentence_sigma=0.9)
    >>> for s in sentences:
    ...  print(s)
    ...
    (10, u'Mus, orci a duis parturient eget tellus vestibulum neque erat.')
    (2, u'Scelerisque gravida.')
    (6, u'Sed parturient hymenaeos, diam blandit ac.')
    (5, u'Viverra nisi, ve praesent dolor.')
    (7, u'Morbi eget dui commodo ve amet ipsum.')
    (2, u'Tincidunt, mi.')
    >>>
    >>> # If you'd like to get the famous incipit, only the first sentence will
    >>> # have it
    >>> sentences = loremipsum.generate_sentences(5,
    ...                                           incipit=True,
    ...                                           sentence_mean=0.9,
    ...                                           sentence_sigma=0.9)
    >>> for s in sentences:
    ...  print(s)
    ...
    (4, u'Lorem ipsum dolor sit.')
    (4, u'Vitae vehicula in, ipsum.')
    (5, u'Velit, risus dictumst orci sociis.')
    (2, u'Nisl ullamcorper.')
    (7, u'Potenti, habitant iaculis dolor felis nam arcu.')
    """
    return _LOREMIPSUM.generate_sentences(amount, **args)


def generate_paragraph(**args):
    """Create a single plausible latin paragraph, with stats.

    The generated text is a single line paragraph and is returned along with
    the amount of sentences and words used. This function accepts the same
    arguments and returns the same as as
    :py:meth:`Generator.generate_paragraph`.

    :rtype: tuple

    >>> import loremipsum
    >>>
    >>> # You can just get a paragraph.
    >>> paragraph = loremipsum.get_paragraph()
    >>>
    >>> # Since default paragraph would be quite a long text...
    >>> loremipsum.get_paragraph(incipit=True
    ...                          paragraph_mean=0.9,
    ...                          paragraph_sigma=0.9,
    ...                          sentence_mean=1.5,
    ...                          sentence_sigma=1.5)
    (3, 10, u'Lorem ipsum dolor. Porta et quam. Lectus at pulvinar nisi.')
    """
    return _LOREMIPSUM.generate_paragraph(**args)


def generate_paragraphs(amount, **args):
    """Creates a generator of plausible latin paragraphs, with stats.

    The generator will produce the specified amount of paragraphs with stats.
    This function accepts the same arguments and returns the same as as
    :py:meth:`Generator.generate_paragraphs`.

    :rtype: generator

    >>> import loremipsum
    >>>
    >>> generated = loremipsum.generate_paragraphs(3)
    >>> for sentences_count, words_count, paragraph in generated:
    ...  print(sentences_count, words_count, len(paragraph))
    14 129 868
    10 100 667
    19 170 1141
    """
    return _LOREMIPSUM.generate_paragraphs(amount, **args)
