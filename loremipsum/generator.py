"""
This module exposes the 2 classes used to generate random plausible text:

:``Sample``:
    Provides the API to extract, load, and dump all the needed informations
    from a sample.
:``Generator``:
    Provides the API to actually generate the text, using a sample.
"""

from __future__ import unicode_literals
import collections
import contextlib
import math
import random
import re
import sys

from loremipsum.serialization import schemes

__all__ = ['Generator', 'Sample']

builtins = sys.modules.get('__builtin__', sys.modules.get('builtins'))
_urlparse = 'urlparse' if sys.version_info[0] == 2 else 'urllib.parse'
_urlparse = __import__(_urlparse, fromlist=_urlparse.split('.')[:1]).urlparse
_irange = getattr(builtins, 'xrange', range)


def _mean(values):
    """Calculate the mean value of a list of integers."""
    return sum(values) / float(len(values))


def _sigma(values):
    """Calculate the sigma value of a list of integers."""
    return math.sqrt(_mean([v ** 2 for v in values]) - _mean(values) ** 2)


class Sample(object):
    """The sample that generated sentences are based on.

    :param tuple frozen:                An immutable representation of the
                                        sample imformations. This argument
                                        takes precedence over any other:
                                        ``sample``, ``text``, ``lexicon``,
                                        ``word_delimiters`` and
                                        ``sentence_delimiters`` will be
                                        ignored.
    :param dict sample:                 A dictionary of the sample internal
                                        state. If ``sample`` is suplpyed,
                                        ``text``, ``lexicon``,
                                        ``word_delimiters`` and
                                        ``sentence_delimiters``
                                        will be ignored.
    :param str text:                    A string containing the sample text.
                                        Sample text must contain one or more
                                        empty-line delimited paragraphs. Each
                                        paragraph must contain one or more
                                        sentences, delimited by any character
                                        included in the ``sentence_delimiters``
                                        argument. Sentences must contains words
                                        included in ``lexicon`` and any
                                        character included in
                                        ``word_delimiters`` argument.
    :param str lexicon:                 A list of strings to be used as words.
    :param str word_delimiters:         A string of characters used as word
                                        delimiters.
    :param str sentence_delimiters:     A string of characters used as sentence
                                        delimiters.
    :raises TypeError:                  If neither frozen nor sample are
                                        provided and any of text, lexicon,
                                        word_delimiters or sentence_delimiters
                                        are missing.
    :raises ValueError:                 If could not succesfully create an
                                        internal :py:class:`Sample` out of the
                                        supplied arguments.

    Text will be generated so that it will have a similar distribution
    of word, sentence and paragraph lengths and punctuation as the sample.

    Sample's ``text`` will be analysed to generate Markov chains that in turn
    will be used to generate the random text. In the analysis, only paragraph,
    sentence and word lengths, and some basic punctuation matter -- the actual
    words are ignored. A provided list of words, the ``lexicon``, will be used
    to generate the random text, so that it will have a similar distribution of
    paragraph, sentence and word lengths.

    ``Sample`` instances behave like read-only dictionay and can be hashed.
    """

    def __init__(self, **args):
        frozen = args.get('frozen')
        sample = args.get('sample')
        text = args.get('text')
        lexicon = args.get('lexicon')
        word_delimiters = args.get('word_delimiters')
        sentence_delimiters = args.get('sentence_delimiters')
        ingredients = [text, lexicon, word_delimiters, sentence_delimiters]
        if frozen:
            self._reheat(frozen)
        elif sample:
            if isinstance(sample, self.__class__):
                self._s = sample._s.copy()
            else:
                self._s = dict()
                self._s.update(sample)
        elif all(ingredients):
            self._cook(*ingredients)
        else:
            raise TypeError('Missing argument')
        self._hash = hash(self.frozen())

    def _cook(self, text, lexicon, word_delimiters, sentence_delimiters):
        """Builds the internal state using the provided arguments."""

        paragraphs_lens = list()
        sentences_lens = list()
        previous = (0, 0)

        us = lambda s: getattr(builtins, 'unicode', str)(s).strip('\n')
        self._s = {
            'text': us(text),
            'lexicon': us(lexicon),
            'word_delimiters': us(word_delimiters),
            'sentence_delimiters': us(sentence_delimiters)}

        # Chains of three words that appear in the sample text
        # Maps a pair of word-lengths to a third word-length and an optional
        # piece of trailing punctuation (for example, a period, comma, etc.)
        self._s['chains'] = chains = collections.defaultdict(list)

        # Pairs of word-lengths that can appear at the beginning of sentences
        self._s['starts'] = starts = [previous]

        # Words that can be used in the generated output
        # Maps a word-length to a list of words of that length
        self._s['dictionary'] = dict()
        for word in self._s['lexicon'].split():
            self._s['dictionary'].setdefault(len(word), list()).append(word)

        for paragraph in self._s['text'].split('\n\n'):

            # We've got a paragraph, so prepare to count sentences.
            paragraphs_lens.append(0)

            for sentence in self._find_sentences(paragraph.strip()):

                # We've got a sentence, so prepare to count words an increas
                # paragraph length.
                sentences_lens.append(0)
                paragraphs_lens[-1] += 1

                # First sentence ever will be set as sample incipit.
                self._s.setdefault('incipit', sentence.group(0))

                # Generates the chains and starts values required for sentence
                # generation.
                for word in self._find_words(sentence.group(0)):

                    # We've got a word, so increas sentence length.
                    sentences_lens[-1] += 1

                    # Build chains and starts based on text analysis.
                    word, delimiter = word.group(0).strip(), ''
                    while word and word[-1] in self._s['word_delimiters']:
                        word, delimiter = word[:-1], word[-1]
                    if word:
                        chains[previous].append((len(word), delimiter))
                        if delimiter:
                            starts.append(previous)
                        previous = (previous[1], len(word))

        # Calculates the mean and standard deviation of the lengths of
        # sentences (in words) in a sample text.
        self._s['sentence_mean'] = _mean(sentences_lens)
        self._s['sentence_sigma'] = _sigma(sentences_lens)

        # Calculates the mean and standard deviation of the lengths of
        # paragraphs (in sentences) in a sample text.
        self._s['paragraph_mean'] = _mean(paragraphs_lens)
        self._s['paragraph_sigma'] = _sigma(paragraphs_lens)
        self._taste()

    def _reheat(self, frozen):
        """Builds the internal state using a frozen sample."""

        _s = dict(frozen)
        _s['chains'] = dict((tuple(k), v) for k, v in _s['chains'])
        for chain, values in _s['chains'].items():
            _s['chains'][chain] = [tuple(v) for v in values]
        _s['starts'] = [tuple(s) for s in _s['starts']]
        _s['dictionary'] = dict(_s['dictionary'])
        self._s = _s
        self._taste()

    def _taste(self):
        """Self check."""

        if not self._s['dictionary']:
            raise ValueError("Invalid lexicon")
        if not self._s['chains']:
            raise ValueError("Invalid sample text")

    def _find_sentences(self, text):
        """Creates an iterator over text, which yields sentences."""

        delimiters = '\\'.join(self._s['sentence_delimiters'])
        sentences = re.compile(r'([^\\{d}])*[\\{d}]'.format(d=delimiters))
        return sentences.finditer(text.strip())

    def _find_words(self, text):
        """Creates an iterator over text, which yields words."""

        words = re.compile(r'\s*([\S]+)')
        return words.finditer(text.strip())

    def row(self):
        """Returns the row components of a sample.

        :returns:   text, lexicon, word_delimiters, sentence_delimiters
        :rtype:     tuple

        The row components are those strictly necessary to build the internal
        state of a :py:class:`Sample`.
        """
        return (
            self._s['text'],
            self._s['lexicon'],
            self._s['word_delimiters'],
            self._s['sentence_delimiters'])

    def frozen(self):
        """Returns a frozen representation of itself.

        :rtype:     tuple of tuples

        Basically this method turns the internal dictionary of the sample state
        into tuples of tuples, allowing an easier serialization.
        """
        _s = self._s.copy()
        ts = lambda i: tuple(sorted(i))
        _s['chains'] = ts((k, ts(v)) for k, v in _s['chains'].items())
        _s['dictionary'] = ts((k, ts(v)) for k, v in _s['dictionary'].items())
        _s['starts'] = ts(_s['starts'])
        return ts(_s.items())

    def copy(self):
        """Returns a :py:class:`dict`  representation (shallow copy) of itself.

        :rtype:     dict
        """
        return self._s.copy()

    @classmethod
    def cooked(class_, text, lexicon, word_delimiters, sentence_delimiters):
        """Returns a :py:class:`Sample` instance based on arguments.

        :param text:                See :py:class:`Sample` keyword arguments.
        :param lexicon:             See :py:class:`Sample` keyword arguments.
        :param word_delimiters:     See :py:class:`Sample` keyword arguments.
        :param sentence_delimiters: See :py:class:`Sample` keyword arguments.

        See :py:meth:`Sample.row` for more informations.

        >>> def resource(name):
        ...     with open(name, 'rb') as txt
        ...         content = txt.read().decode('UTF-8')
        ...     return content
        ...
        >>> text = resource('sample.txt')
        >>> lexicon = resource('lexicon.txt')
        >>> w_delimiters = resource('word_delimiters.txt')
        >>> s_delimiters = resource('sentence_delimiters.txt')
        >>> sample = Sample.cooked(text, lexicon, w_delimiters, s_delimiters)

        Also, you can do:

        >>> other = loremipsum.samples.get(name)
        >>> type(other)
        <class 'loremipsum.generator.Sample'>
        >>> sample = Sample.cooked(*other.row())
        >>>
        """
        return class_(
            text=text,
            lexicon=lexicon,
            word_delimiters=word_delimiters,
            sentence_delimiters=sentence_delimiters)

    @classmethod
    def thawed(class_, frozen):
        """Returns a :py:class:`Sample` instance based on the frozen sample.

        :param frozen:  A frozen representation of a sample: a tuple of tuples.

        See :py:meth:`Sample.frozen` for more informations.

        >>> other = loremipsum.samples.get(name)
        >>> type(other)
        <class 'loremipsum.generator.Sample'>
        >>> sample = Sample.thawed(other.frozen())
        >>>
        """
        return class_(frozen=frozen)

    @classmethod
    def duplicated(class_, sample):
        """Returns a :py:class:`Sample` instance based on a mapping.

        :param sample:  Can be a :py:class:`dict` or a :py:class:`Sample`.

        See :py:meth:`Sample.frozen` for more informations.

        >>> other = loremipsum.samples.get(name)
        >>> type(other)
        <class 'loremipsum.generator.Sample'>
        >>> sample = Sample.duplicated(other.copy())
        >>>
        """
        return class_(sample=sample)

    @classmethod
    def load(class_, url, **args):
        """Loads a sample from an URL.

        :param str url:             The URL of the sample.
        :returns:                   A ``class_`` instance.
        :raises AttributeError:     If could not find specified ``scheme``,
                                    ``content_type`` or ``content_encoding``

        Base keyword arguments:

        :content_type:
            Force the content to be handled as specified. The value of
            this keyword must be a string containig the internet media type
            that you want to be used: ``<type>/<sub-type>``. If this keyword
            argument is not specified, it will be guessed using the URL.
        :content_encoding:
            Force the content encoding to be handled as specified. By content
            encoding, basically, we mean compression method. If this keyword
            argument is not specified, it will be guessed using the URL.

        Other keyword arguments are passed to the handlers. See their
        respective documentation.

        By default, ``content_type`` and ``content_encoding`` guessing should
        be done by :py:func:`mimetypes.guess_type`.  Refer to each scheme
        documentation for more information.
        """
        url = _urlparse(url)
        return schemes.get(url.scheme).load(class_, url, **args)

    def dump(self, url, **args):
        """Dumps a sample to an URL.

        :param str url:             The URL of the sample.
        :raises AttributeError:     If could not find specified ``scheme``,
                                    ``content_type`` or ``content_encoding``

        Read :py:meth:`load` for more information about keyword arguments and
        ``content_type`` or ``content_encoding`` guessing.
        """
        url = _urlparse(url)
        schemes.get(url.scheme).dump(self, url, **args)

    @staticmethod
    def remove(url, **args):
        """Remove a dumped sample from a URL.

        :param str url:             The URL of the sample.
        :raises AttributeError:     If could not find specified ``scheme``,
                                    ``content_type`` or ``content_encoding``

        Read :py:meth:`load` for more information about keyword arguments and
        ``content_type`` or ``content_encoding`` guessing.
        """
        url = _urlparse(url)
        schemes.get(url.scheme).remove(url, **args)

    def __getitem__(self, key):
        return self._s[key]

    def __iter__(self):
        return self._s.__iter__()

    def __len__(self):
        return self._s.__len__()

    def __hash__(self):
        return hash(self.frozen())

    def __eq__(self, other):
        return self._hash == hash(other)


class Generator(object):
    """Generates random strings of plausible text.

    :param sample:  A :py:class:`Sample` that will provide all the needed info
                    to generate the text.

    The attributes of this class should be considered 'read-only'. Even if
    you can access the internal state of the generator, you don't want to mess
    with it: we are all grown adults.
    """

    def __init__(self, sample=None):
        self._sample = sample

    @property
    def sample(self):
        return self._sample

    @sample.setter
    def sample(self, value):
        if isinstance(value, dict):
            self._sample = Sample.duplicated(value)
        elif isinstance(value, tuple):
            try:
                # If value is row it won't have cooked up keys, so KeyError
                # will be raised.
                self._sample = Sample.thawed(value)
            except ValueError:
                self._sample = Sample.cooked(*value)
        elif isinstance(value, Sample):
            self._sample = value
        else:
            raise ValueError(type(value))

    @contextlib.contextmanager
    def default(self, **args):
        """Context manager. Yields a :py:class:`Generator` with altered defaults.

        The purpose of this method is to let the call of more
        :py:class:`Generator` methods with predefined set of arguments.

        >>> from loremipsum import generator
        >>> from loremipsum import samples
        >>> g = generator.Generator(samples.DEFAULT)
        >>> with g.default(sentence_sigma=0.9, sentence_mean=0.9) as short:
        ...     sentences = short.generate_sentences(3)
        ...     paragraps = short.generate_paragraphs(5, incipit=True)
        ...
        """
        copy = self._sample._s.copy()
        copy.update(args)
        yield Generator(sample=Sample(sample=copy))

    def generate_word(self, length=None):
        """Selects a random word from the lexicon.

        :param int length:  the length of the generate word
        :rtype:             str or unicode or None
        """

        dictionary = self._sample['dictionary']
        if not length:
            length = random.choice(list(dictionary))
        return random.choice(dictionary.get(length, (None,)))

    def generate_words(self, amount, length=None):
        """Creates a generatator of the specified amount of words.

        :param int amount:  the amount of words to be generated
        :rtype:             generator

        Words are randomly selected from the lexicon. Also accepts length
        argument as per :py:meth:`generate_word`.
        """

        for __ in _irange(amount):
            yield self.generate_word(length)

    def generate_sentence(self, **args):
        """Generates a single sentence, of random length.

        :param bool incipit:            If True, then the text will begin with
                                        the sample text incipit sentence.
        :param int sentence_len:        The length of the sentence in words.
                                        Takes precedence over sentence_mean and
                                        sentence_sigma.
        :param float sentence_mean:     Override the sentence mean value.
        :param float sentence_sigma:    Override the sentence sigma value.
        :retruns:                       A tuple containing sentence length and
                                        sentence text.
        :rtype:                         tuple(int, str or unicode)
        """

        # The length of the sentence is a normally distributed random variable.
        mean = args.get('sentence_mean', self._sample['sentence_mean'])
        sigma = args.get('sentence_sigma', self._sample['sentence_sigma'])
        incipit = args.get('incipit', False)
        random_len = max(2, int(round(abs(random.normalvariate(mean, sigma)))))
        sentence_len = args.get('sentence_len', random_len)
        previous_set = set(self._sample['chains']) & set(self._sample['starts'])
        words = list()
        previous = tuple()
        last_word = ''
        dictionary = self._sample['dictionary']

        # Defined here in case while loop doesn't run
        word_delimiter = ''

        # Start the sentence with sample incipit, if desired
        if incipit:
            words.extend(self.sample['incipit'].split()[:sentence_len])
            if words[-1][-1] in self.sample['word_delimiters']:
                word_delimiter = words[-1][-1]

        # Generate a sentence from the "chains"
        for __ in _irange(sentence_len - len(words)):
            # If the current starting point is invalid, choose another randomly
            if previous not in self._sample['chains']:
                previous = random.sample(previous_set, 1)[0]

            # Choose the next "chain" to go to. This determines the next word
            # length we'll use, and whether there is e.g. a comma at the end of
            # the word.
            chain = random.choice(self._sample['chains'][previous])
            word_len = chain[0]

            # If the word delimiter contained in the chain is also a sentence
            # delimiter, then we don't include it because we don't want the
            # sentence to end prematurely (we want the length to match the
            # sentence_len value).
            word_delimiter = ''
            if chain[1] not in self.sample['sentence_delimiters']:
                word_delimiter = chain[1]

            # Choose a word randomly that matches (or closely matches) the
            # length we're after.
            closest = min(list(dictionary), key=lambda x: abs(x - word_len))

            # Readability. No word can appear next to itself.
            word = random.choice(dictionary[closest])
            while word == last_word and len(dictionary[closest]) > 1:
                word = random.choice(dictionary[closest])
            last_word = word

            words.append(word + word_delimiter)
            previous = (previous[1], word_len)

        # Finish the sentence off with capitalisation, a period and
        # form it into a string.
        # TODO(sentence_delimiters): should analyze sample to randomize
        #                            sentence delimiter choice.
        sentence = ' '.join(words).capitalize().rstrip(word_delimiter) + '.'
        return (len(words), sentence)

    def generate_sentences(self, amount, **args):
        """Generator method that yields sentences, of random length.

        :param int amount:              The amouont of sentences to generate
        :retruns:                       A generator of specified amount tuples
                                        as per :py:meth:`generate_sentence`.
        :rtype:                         generator

        Also accepts the same arguments as :py:meth:`generate_sentence`.
        """
        yield self.generate_sentence(**args)
        args['incipit'] = False
        for __ in _irange(amount - 1):
            yield self.generate_sentence(**args)

    def generate_paragraph(self, **args):
        """Generates a single paragraph, of random length.

        :param int paragraph_len:       The length of the paragraph in
                                        sentences. Takes precedence over
                                        paragraph_mean and paragraph_sigma.
        :param float paragraph_mean:    Override the paragraph mean value.
        :param float paragraph_sigma:   Override the paragraph sigma value.
        :returns:                       A tuple containing number of sentences,
                                        number of words, and the paragraph
                                        text.
        :rtype:                         tuple(int, int, str or unicode)

        Also accepts the same arguments as :py:meth:`generate_sentence`.
        """
        # The length of the paragraph is a normally distributed random
        # variable.
        mean = args.get('paragraph_mean', self._sample['paragraph_mean'])
        sigma = args.get('paragraph_sigma', self._sample['paragraph_sigma'])
        random_len = max(2, int(round(abs(random.normalvariate(mean, sigma)))))
        paragraph_len = args.get('paragraph_len', random_len)

        words_count = 0
        paragraph = list()

        for count, text in self.generate_sentences(paragraph_len, **args):
            words_count += count
            paragraph.append(text)

        # Turn the paragraph into a string.
        return (paragraph_len, words_count, ' '.join(paragraph))

    def generate_paragraphs(self, amount, **args):
        """Generator method that yields paragraphs, of random length.

        :param int amount:              The amount of paragraphs to generate.
        :retruns:                       A generator of specified amount tuples.
                                        as per :py:meth:`generate_paragraph`
        :rtype:                         generator

        Also accepts the same arguments as :py:meth:`generate_paragraph`.
        """
        yield self.generate_paragraph(**args)
        args['incipit'] = False
        for __ in _irange(amount - 1):
            yield self.generate_paragraph(**args)
