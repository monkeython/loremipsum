"""
The purpose of the ``loremipsum`` package is to provide high level API to a
:py:class:`loremipsum.generator.Generator` that returns random plausible text
based on a sample. There are 2 sets of functions:

* Those with ``get_`` prefixed functions that return the desired text
* Those with ``generate_`` prefixed functions that also return additional
  informations like the number of words or sentences used.

So, on the average, you probably want to use the ``get_`` prefixed functions and
just get the text:

>>> sentences_list = list(loremipsum.get_sentences(5))
>>> len(sentences_list)
5
>>>

Otherwise, if you fancy some info on the generated text, you want to use the
``generate_`` prefixed functions:

>>> sentences_count, words_count, paragraph = loremipsum.generate_paragraph()
>>> sentences_count
11
>>> words_count
109
>>> len(paragraph)
695

The above mentioned functions will generate text using the default sample,
which is a pseudo latin text known as `Lorem Ipsum`_. The
:py:mod:`loremipsum.samples` pluggable sub-package expose simple functions to
browse, get any or set default plugged samples. Setting a different default
sample will, of course, affect the text generated by the functions in this
package.  :py:mod:`loremipsum.generator`, instead, exposes a lower level API to
help you to create, load, dump and use your own samples and text generators.

.. _`Lorem Ipsum`: http://en.wikipedia.org/wiki/Lorem_ipsum
"""

__author__ = "Luca De Vitis <luca@monkeython.com>"
__version__ = '2.0.0b2'
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

from loremipsum import generator
from loremipsum import samples
from loremipsum import serialization

import collections
import functools
import string

import pkg_resources

# Declaring the package public API
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
    'generator',
    'samples',
    'serialization']


# Plugin register
_PLUGS = collections.defaultdict(dict)


def _plugs_get(name, default=None, package=None):
    """Returns the desired plugged in object.

    :param str name:    The plugin name.
    :param default:     The default value to return if lookup fails.
    :returns:           The plugged in object.
    """
    maketrans = getattr(string, 'maketrans', getattr(str, 'maketrans', None))
    name = name.translate(maketrans("/-", "__"))
    return _PLUGS[package.__name__].get(name, default)


def _plugs_set_default(name, package=None):
    """Set the default plugin.

    :param str name:    The plugin name.
    """
    package.DEFAULT = _plugs_get(name, None, package)


def _plugs_registered(package=None):
    """Returns a dictionary of the registered plugins.

    :returns:           dict
    """
    return _PLUGS[package.__name__].copy()


def _plugs_init(package):
    """Set the package up for plugins management.

    Makes the following functions available:
    * ``package.get``
    * ``package.set_default``
    * ``package.registered``

    :param package:     The package object to setup for plugins.
    """

    package.DEFAULT = None
    package.get = functools.partial(_plugs_get, package=package)
    package.set_default = functools.partial(_plugs_set_default, package=package)
    package.registered = functools.partial(_plugs_registered, package=package)

    for module_name in package.__all__:
        name, value = module_name.rstrip('_'), getattr(package, module_name)
        _PLUGS[package.__name__][name] = value

    plugins = pkg_resources.iter_entry_points(package.__name__)
    _PLUGS[package.__name__].update(p for p in plugins)

# Setting up the plugs
_plugs_init(samples)
_plugs_init(serialization.schemes)
_plugs_init(serialization.content_types)
_plugs_init(serialization.content_encodings)

# Setting the plugs defaults
serialization.schemes.set_default('file')
serialization.content_types.set_default('application/json')
serialization.content_encodings.set_default('gzip')
samples.set_default('loremipsum')


def get_word(length=None):
    """Selects a random word from the from the sample lexicon.

    This function accepts the same arguments and returns the same as
    :py:meth:`Generator.generate_word`.

    :rtype: str or unicode

    Just get a word:

    >>> loremipsum.get_word()
    u'neque'
    >>>

    Get a 6 charaters long word:

    >>> loremipsum.get_word(6)
    u'turpis'
    >>>
    """
    default = generator.Generator(samples.DEFAULT)
    return default.generate_word(length)


def get_words(amount, length=None):
    """Creates a generatator of the specified amount of words.

    This function accepts the same arguments and returns the same as
    :py:meth:`Generator.generate_words`.

    :rtype: generator

    Just get 3 words:

    >>> list(loremipsum.get_words(3))
    [u'lorem', u'fringilla', u'class']
    >>>

    Get 4 words that are 5 charaters long:

    >>> list(loremipsum.get_words(4, 5))
    [u'justo', u'curae', u'morbi', u'porta']
    >>>
    """
    default = generator.Generator(samples.DEFAULT)
    return default.generate_words(amount, length)


def get_sentence(**args):
    """Creates a single plausible sentence.

    This function accepts the same arguments as
    :py:meth:`Generator.generate_sentence`.

    :rtype: str or unicode

    Just get a sentence:

    >>> loremipsum.get_sentence()
    u'Laoreet nulla sed donec dis magna nisi mauris, aliquam urna donec vel.'
    >>>

    You can make it startss with the sample incipit:

    >>> loremipsum.get_sentence(incipit=True)
    u'Lorem ipsum dolor sit.'
    >>>

    Or you can force its length:

    >>> loremipsum.get_sentence(sentence_len=5)
    u'Praesent vulputate massa porta nullam.'
    >>>
    """
    default = generator.Generator(samples.DEFAULT)
    return default.generate_sentence(**args)[-1]


def get_sentences(amount, **args):
    """Creates a generator of plausible sentences.

    The generator yields only the sentences text. This function
    accepts the same arguments as :py:meth:`Generator.generate_sentences`.

    :rtype: generator

    Get a generator of sentence:

    >>> for sentence in loremipsum.get_sentences(3):
    ...     print(sentence)
    ...
    Nisi pede erat justo tristique nascetur.
    Sodales, felis aliquet quisque porta urna magna.
    Risus proin montes velit felis non eget leo.
    >>>

    Should you ever need, you can adjust mean and sigma values to alter
    the random words count in a sentence. The following should generate
    quite short sentences:

    >>> short = dict(sentence_mean=0.9, sentence_sigma=0.9)
    >>> for sentence in loremipsum.get_sentences(10, **short):
    ...     print(sentence)
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

    If you'd like to get the sample incipit, only the first sentence will
    have it:

    >>> short = dict(sentence_mean=0.9, sentence_sigma=0.9, incipit=True)
    >>> for sentence in loremipsum.get_sentences(5, **short):
    ...     print(sentence)
    ...
    Lorem ipsum dolor.
    At, tempor potenti.
    Pellentesque quisque duis.
    Condimentum accumsan laoreet.
    Suscipit pede.
    """
    default = generator.Generator(samples.DEFAULT)
    for sentence in default.generate_sentences(amount, **args):
        yield sentence[-1]


def get_paragraph(**args):
    """Creates a single plausible paragraph.

    This function accepts the same arguments as
    :py:meth:`Generator.generate_paragraph`.

    :rtype: str or unicode

    You can just get a paragraph:

    >>> paragraph = loremipsum.get_paragraph()
    >>> len(paragraph)
    735
    >>>

    Since default paragraph would be quite a long text:

    >>> loremipsum.get_paragraph(paragraph_mean=0.9,
    ...                          paragraph_sigma=0.9,
    ...                          sentence_mean=1.5,
    ...                          sentence_sigma=1.5)
    u'Ut quam. Netus ac. Commodo, porta risus conubia.'
    """
    default = generator.Generator(samples.DEFAULT)
    return default.generate_paragraph(**args)[-1]


def get_paragraphs(amount, **args):
    """Creates a generator of plausible paragraphs.

    The generator yields only the paragraphs text. This function accepts the
    same arguments as :py:meth:`Generator.generate_paragraph`.

    :rtype: generator

    >>> len('\n\n'.join(list(loremipsum.get_paragraphs(3))))
    2475
    """
    default = generator.Generator(samples.DEFAULT)
    for paragraph in default.generate_paragraphs(amount, **args):
        yield paragraph[-1]


def generate_sentence(**args):
    """Returns a single plausible sentence text with sentence info.

    The created sentence is returned along with the amount of words used. This
    function accepts the same arguments and returns the same as
    :py:meth:`Generator.generate_sentence`.

    :rtype: tuple

    Generate a tuple containing the words count and the sentence text:

    >>> words_count, sentence = loremipsum.generate_sentence()
    >>> words_count
    8
    >>> sentence
    u'Conubia euismod orci eros, suscipit tortor, magna tincidunt.'
    >>>

    You can make it startss with sample incipit:

    >>> loremipsum.generate_sentence(incipit=True)
    (7, u'Lorem ipsum dolor sit amet, consectetuer adipiscing.')
    >>>

    Or you can force its length:

    >>> loremipsum.generate_sentence(sentence_len=5)
    (5, u'Pede, nisl dolor nisl congue.')
    """
    default = generator.Generator(samples.DEFAULT)
    return default.generate_sentence(**args)


def generate_sentences(amount, **args):
    """Creates a generator of plausible latin sentences, with stats.

    The generator will produce the specified amount of sentences with stats.
    This function accepts the same arguments and returns the same as
    as :py:meth:`Generator.generate_sentences`.

    :rtype: generator

    Get a list of sentence and respective info:

    >>> for generated in loremipsum.generate_sentences(3):
    ...     print(generated)
    ...
    (5, u'Pharetra, in, odio fermentum id.')
    (10, u'Amet fames dolor, aptent curae ad auctor dui congue, cum.')
    (9, u'Fames turpis curae morbi senectus dolor cum pede facilisis.')
    >>>

    As for the :py:func:`loremipsum.get_sentences` function, you can adjust
    mean and sigma values to alter the random words count in a sentence. The
    following should generate rather shot sentences:

    >>> short = dict(sentence_mean=0.9, sentence_sigma=0.9)
    >>> for sentence in loremipsum.generate_sentences(6, **short):
    ...     print(sentence)
    ...
    (10, u'Mus, orci a duis parturient eget tellus vestibulum neque erat.')
    (2, u'Scelerisque gravida.')
    (6, u'Sed parturient hymenaeos, diam blandit ac.')
    (5, u'Viverra nisi, ve praesent dolor.')
    (7, u'Morbi eget dui commodo ve amet ipsum.')
    (2, u'Tincidunt, mi.')
    >>>

    If you'd like to get the famous incipit, only the first sentence will
    have it:

    >>> short = dict(incipit=True, sentence_mean=0.9, sentence_sigma=0.9)
    >>> for sentence in loremipsum.generate_sentences(5, **short):
    ...     print(sentence)
    ...
    (4, u'Lorem ipsum dolor sit.')
    (4, u'Vitae vehicula in, ipsum.')
    (5, u'Velit, risus dictumst orci sociis.')
    (2, u'Nisl ullamcorper.')
    (7, u'Potenti, habitant iaculis dolor felis nam arcu.')
    """
    default = generator.Generator(samples.DEFAULT)
    return default.generate_sentences(amount, **args)


def generate_paragraph(**args):
    """Create a single plausible latin paragraph, with stats.

    The generated text is a single line paragraph and is returned along with
    the amount of sentences and words count. This function accepts the same
    arguments and returns the same as :py:meth:`Generator.generate_paragraph`.

    :rtype: tuple

    You can just generate a paragraph:

    >>> sentences_count, words_count, text = loremipsum.generate_paragraph()
    >>> sentences_count
    4
    >>> words_count
    30
    >>> len(text)
    167
    >>>

    Since default paragraph would be quite a long text:

    >>> loremipsum.generate_paragraph(incipit=True
    ...                               paragraph_mean=0.9,
    ...                               paragraph_sigma=0.9,
    ...                               sentence_mean=1.5,
    ...                               sentence_sigma=1.5)
    (3, 10, u'Lorem ipsum dolor. Porta et quam. Lectus at pulvinar nisi.')
    """
    default = generator.Generator(samples.DEFAULT)
    return default.generate_paragraph(**args)


def generate_paragraphs(amount, **args):
    """Creates a generator of plausible latin paragraphs, with stats.

    The generator will produce the specified amount of paragraphs with stats.
    This function accepts the same arguments and returns the same as as
    :py:meth:`Generator.generate_paragraphs`.

    :rtype: generator

    >>> generated = loremipsum.generate_paragraphs(3)
    >>> for sentences_count, words_count, paragraph in generated:
    ...     print(sentences_count, words_count, len(paragraph))
    14 129 868
    10 100 667
    19 170 1141
    """
    default = generator.Generator(samples.DEFAULT)
    return default.generate_paragraphs(amount, **args)
