"""
This package provides a text generator class and some utility functions that
can simply return the text you desire. There are 2 sets of functions:

* Those with **generate_** prefix that return the desired text and some stats
* Those with **get_** that return the desired text without the stats

On the average, you probably want to import the **get_** prefixed functions and
just get the text:

>>> import loremipsum
>>>
>>> sentences_list = loremipsum.get_sentences(5)
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
>>> with open('data/sample.txt', 'rb') as sample_txt
>>>     sample = sample_txt.read().decode('utf-8')
>>> with open('data/lexicon.txt', 'rb') as lexicon_txt
>>>     dictionary = lexicon_txt.read().decode('utf-8').split()
>>>
>>> sentence_delimiters = '.?!'
>>> word_relimiters = ',' + sentence_delimiters
>>> g = loremipsum.Generator(sample, dictionary,
...                          word_relimiters, sentence_delimiters)
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

from loremipsum import generator
from loremipsum import samples
from loremipsum import serialization
from loremipsum import tests

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
    'serialization',
    'tests']


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
    * package.get
    * package.set_default
    * package.registered

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
    default = generator.Generator(samples.DEFAULT)
    return default.generate_word(length)


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
    default = generator.Generator(samples.DEFAULT)
    return default.generate_words(amount, length)


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
    default = generator.Generator(samples.DEFAULT)
    return default.generate_sentence(**args)[-1]


def get_sentences(amount, **args):
    """Creates a generator of plausible latin sentences.

    The generator yields only the sentences text. This function
    accepts the same arguments as :py:meth:`Generator.generate_sentences`.

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
    >>> # quite short sentences
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
    default = generator.Generator(samples.DEFAULT)
    for sentence in default.generate_sentences(amount, **args):
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
    default = generator.Generator(samples.DEFAULT)
    return default.generate_paragraph(**args)[-1]


def get_paragraphs(amount, **args):
    """Creates a generator of plausible latin paragraphs.

    The generator yields only the paragraphs text. This function accepts the
    same arguments as :py:meth:`Generator.generate_paragraph`.

    :rtype: generator

    >>> import loremipsum
    >>>
    >>> len('\n\n'.join(list(loremipsum.get_paragraphs(3))))
    2475
    """
    default = generator.Generator(samples.DEFAULT)
    for paragraph in default.generate_paragraphs(amount, **args):
        yield paragraph[-1]


def generate_sentence(**args):
    """Create a single plausible latin sentence, with stats.

    The created sentence is returned along with the amount of words used. This
    function accepts the same arguments and returns the same as
    :py:meth:`Generator.generate_sentence`.

    :rtype: tuple

    >>> import loremipsum
    >>>
    >>> # Generate a tuple containing the words count and the sentence text.
    >>> loremipsum.generate_sentence()
    (8, u'Conubia euismod orci eros, suscipit tortor, magna tincidunt.')
    >>>
    >>> # You can make it startss with famous 'Lorem ipsum' incipit
    >>> loremipsum.generate_sentence(incipit=True)
    (7, u'Lorem ipsum dolor sit amet, consectetuer adipiscing.')
    >>>
    >>> # Or you can force its length
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
    >>> # As for the get_sentences function, you can adjust mean and sigma
    >>> # values to alter the random words count in a sentence. The following
    >>> # should generate rather shot sentences.
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
    default = generator.Generator(samples.DEFAULT)
    return default.generate_sentences(amount, **args)


def generate_paragraph(**args):
    """Create a single plausible latin paragraph, with stats.

    The generated text is a single line paragraph and is returned along with
    the amount of sentences and words count. This function accepts the same
    arguments and returns the same as :py:meth:`Generator.generate_paragraph`.

    :rtype: tuple

    >>> import loremipsum
    >>>
    >>> # You can just generate a paragraph.
    >>> sentences_count, words_count, text = loremipsum.generate_paragraph()
    >>>
    >>> # Since default paragraph would be quite a long text...
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

    >>> import loremipsum
    >>>
    >>> generated = loremipsum.generate_paragraphs(3)
    >>> for sentences_count, words_count, paragraph in generated:
    ...  print(sentences_count, words_count, len(paragraph))
    14 129 868
    10 100 667
    19 170 1141
    """
    default = generator.Generator(samples.DEFAULT)
    return default.generate_paragraphs(amount, **args)
