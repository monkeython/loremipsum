"""
This module provides a simple class to generate plausible text paragraphs,
sentences, or just random words out of a sample text and a sample lexicon.
"""

from __future__ import unicode_literals
import math
import random
import re
import sys

__all__ = ['Generator']

ceil = math.ceil
sqrt = math.sqrt
choice = random.choice
normalvariate = random.normalvariate
unicode_str = sys.version_info[0] == 3 and str or unicode


def _sentences_finditer(generator, text):
    """Creates an iterator over text, which yields sentences."""
    sentences = re.compile(r'([^\\{d}])*[\\{d}]'.format(
        d='\\'.join(generator._gen['delimiters']['sentence'])))
    return sentences.finditer(text.strip())


def _words_finditer(text):
    """Creates an iterator over text, which yields words."""
    words = re.compile(r'\s*([\S]+)')
    return words.finditer(text.strip())


def _mean(values):
    """Calculate the mean value of a list of integers."""
    return sum(values) / float(len(values))


def _sigma(values):
    """Calculate the sigma value of a list of integers."""
    variance = _mean([v**2 for v in values]) - _mean(values)**2
    return sqrt(variance)


class Generator(object):
    """Generates random strings of plausible text.

    Markov chains are used to generate the random text based on the analysis of
    a sample text. In the analysis, only paragraph, sentence and word lengths,
    and some basic punctuation matter -- the actual words are ignored. A
    provided list of words is then used to generate the random text, so that it
    will have a similar distribution of paragraph, sentence and word lengths.

    :param str sample:                  A string containing the sample text.
                                        Sample text must contain one or more
                                        empty-line delimited paragraphs. Each
                                        paragraph must contain one or more
                                        sentences, delimited by any char
                                        included in the sentences_delimiters
                                        param.
    :param list lexicon:                A list of strings to be used as words.
    :param list word_delimiters:        A list of strings to be used as word
                                        delimiters.
    :param list sentence_delimiters:    A list of strings to be used as
                                        sentence delimiters.
    """

    def __init__(self, sample, lexicon, word_delimiters, sentence_delimiters):

        self._gen = dict()

        # Statistics for sentence and paragraph generation
        self._gen['sentence'] = dict()
        self._gen['paragraph'] = dict()

        # Words that can be used in the generated output
        # Maps a word-length to a list of words of that length
        self._gen['dictionary'] = dict()

        # The bare list of words
        self._gen['lexicon'] = list()

        # Chains of three words that appear in the sample text
        # Maps a pair of word-lengths to a third word-length and an optional
        # piece of trailing punctuation (for example, a period, comma, etc.)
        self._gen['chains'] = dict()

        # Pairs of word-lengths that can appear at the beginning of sentences
        self._gen['starts'] = set()

        self._gen['delimiters'] = {
            'word': word_delimiters,
            'sentence': sentence_delimiters}

        self._setup_lexicon(lexicon)
        self._setup_sample_text(sample)

    def _setup_lexicon(self, lexicon):
        """Setup the lexicon and dictionary."""

        # Build the lexicon and dictionary.
        for word in lexicon:
            word = unicode_str(word.strip())
            if word:
                self._gen['dictionary'].setdefault(len(word), []).append(word)
                self._gen['lexicon'].append(word)

        self._gen['lexicon'] = tuple(self._gen['lexicon'])

        if not self._gen['lexicon']:
            raise ValueError("Empty lexicon")

    def _setup_sample_text(self, sample):
        """Setup the chains and the stats needed to generate text."""

        # Build the saple text info that will be used to generate the sentences
        # and paragraphs.
        previous = (0, 0)
        self._gen['starts'].add(previous)
        paragraphs_lens = list()
        sentences_lens = list()

        sample = unicode_str(sample)

        for paragraph in sample.split('\n\n'):

            # If nusual punctuation...
            # if not paragraph.group(1).strip():
            #     continue

            # We've got a paragraph, so prepare to count sentences.
            paragraphs_lens.append(0)

            for sentence in _sentences_finditer(self, paragraph.strip()):

                # If nusual punctuation...
                # if not sentence.group(1).strip():
                #     continue

                # We've got a sentence, so prepare to count words an increas
                # paragraph length.
                sentences_lens.append(0)
                paragraphs_lens[-1] += 1

                # First sentence ever will be set as sample incipit.
                self._gen.setdefault('incipit', sentence.group(0))

                # Generates the chains and starts values required for sentence
                # generation.
                for word in _words_finditer(sentence.group(0)):

                    # If nusual punctuation...
                    # if not word.group(1).strip():
                    #     continue

                    word = word.group(0).strip()
                    # We've got a word, so increas sentence length.
                    sentences_lens[-1] += 1

                    # Build chains and starts based on text analysis.
                    word_len, delimiter = len(word), ''
                    if word and word[-1] in self._gen['delimiters']['word']:
                        word_len, delimiter = word_len - 1, word[-1]
                    if word_len > 0:
                        chain = self._gen['chains'].setdefault(previous, [])
                        chain.append((word_len, delimiter))
                        if delimiter:
                            self._gen['starts'].add(previous)
                        previous = (previous[1], word_len)

        if self._gen['chains']:

            self._gen['text'] = sample

            # Calculates the mean and standard deviation of the lengths of
            # sentences (in words) in a sample text.
            self._gen['sentence']['mean'] = _mean(sentences_lens)
            self._gen['sentence']['sigma'] = _sigma(sentences_lens)

            # Calculates the mean and standard deviation of the lengths of
            # paragraphs (in sentences) in a sample text.
            self._gen['paragraph']['mean'] = _mean(paragraphs_lens)
            self._gen['paragraph']['sigma'] = _sigma(paragraphs_lens)

        else:
            raise ValueError("The sample text had an unexpected format")

    @property
    def sentence_mean(self):
        """The sample text mean sentence length."""
        return self._gen['sentence']['mean']

    @property
    def sentence_sigma(self):
        """The sample text standard deviation of sentences lengths."""
        return self._gen['sentence']['sigma']

    @property
    def paragraph_mean(self):
        """The sample text mean paragraph length."""
        return self._gen['paragraph']['mean']

    @property
    def paragraph_sigma(self):
        """The sample text standard deviation of paragraphs lengths."""
        return self._gen['paragraph']['sigma']

    @property
    def sample(self):
        """The sample text that generated sentences are based on.

        Sentences are generated so that they will have a similar distribution
        of word, sentence and paragraph lengths and punctuation.

        Sample text should be a string consisting of a number of paragraphs,
        each separated by empty lines. Each paragraph should consist of a
        number of sentences, separated by periods, exclamation marks and/or
        question marks. Sentences consist of words, separated by white space.
        """
        return self._gen['text']

    @property
    def lexicon(self):
        """The plain list of words that can be used in generated text."""
        return self._gen['lexicon']

    @property
    def incipit(self):
        """The first sentence of the sample text."""
        return self._gen['incipit']

    def generate_word(self, length=None):
        """Selects a random word from the lexicon.

        :param int length:  the length of the generate word
        :rtype:             str or unicode or None
        """
        if length:
            return choice(self._gen['dictionary'].get(length, (None,)))
        return choice(self.lexicon)

    def generate_words(self, amount, length=None):
        """Creates a generatator of the specified amount of words.

        Words are randomly selected from the lexicon. Also accepts length
        argument as per :py:meth:`generate_word`.

        :param int amount:  the amount of words to be generated
        :rtype:             generator
        """
        need, more_words = next, iter(range(amount))
        while need(more_words, False) is not False:
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
        mean = args.get('sentence_mean', self.sentence_mean)
        sigma = args.get('sentence_sigma', self.sentence_sigma)
        incipit = args.get('incipit', False)
        sentence_len = int(1 + ceil(abs(normalvariate(mean, sigma))))
        sentence_len = args.get('sentence_len', sentence_len)

        words = []
        previous = ()
        last_word = ''

        # Defined here in case while loop doesn't run
        word_delimiter = ''

        # Start the sentence with sample incipit, if desired
        if incipit:
            words.extend(self.incipit.split()[:sentence_len])
            last_char = words[-1][-1]
            if last_char in self._gen['delimiters']['word']:
                word_delimiter = last_char

        # Generate a sentence from the "chains"
        need, more_words = next, iter(range(sentence_len - len(words)))
        while need(more_words, False) is not False:
            # If the current starting point is invalid, choose another randomly
            if previous not in self._gen['chains']:
                chains = set(self._gen['chains'].keys())
                starts = self._gen['starts']
                previous = choice(list(chains.intersection(starts)))

            # Choose the next "chain" to go to. This determines the next word
            # length we'll use, and whether there is e.g. a comma at the end of
            # the word.
            chain = choice(self._gen['chains'][previous])
            word_len = chain[0]

            # If the word delimiter contained in the chain is also a sentence
            # delimiter, then we don't include it because we don't want the
            # sentence to end prematurely (we want the length to match the
            # sentence_len value).
            if chain[1] in self._gen['delimiters']['sentence']:
                word_delimiter = ''
            else:
                word_delimiter = chain[1]

            # Choose a word randomly that matches (or closely matches) the
            # length we're after.
            dictionary = self._gen['dictionary']
            lengths = list(dictionary.keys())
            closest = lengths[0]
            for length in lengths:
                if abs(word_len - length) < abs(word_len - closest):
                    closest = length

            # Readability. No word can appear next to itself.
            word = choice(dictionary[closest])
            while word == last_word and len(dictionary[closest]) > 1:
                word = choice(dictionary[closest])
            last_word = word

            words.append(word + word_delimiter)
            previous = (previous[1], word_len)

        # Finish the sentence off with capitalisation, a period and
        # form it into a string
        sentence = ' '.join(words).capitalize().rstrip(word_delimiter) + '.'
        return (len(words), sentence)

    def generate_sentences(self, amount, **args):
        """Generator method that yields sentences, of random length.

        Also accepts the same arguments as :py:meth:`generate_sentence`.

        :param int amount:              The amouont of sentences to generate
        :retruns:                       A generator of specified amount tuples
                                        as per :py:meth:`generate_sentence`.
        :rtype:                         generator
        """
        yield self.generate_sentence(**args)
        args['incipit'] = False
        need, more_sentences = next, iter(range(amount - 1))
        while need(more_sentences, False) is not False:
            yield self.generate_sentence(**args)

    def generate_paragraph(self, **args):
        """Generates a single paragraph, of random length.

        Also accepts the same arguments as :py:meth:`generate_sentence`.

        :param int paragraph_len:       The length of the paragraph in
                                        sentences. Takes precedence over
                                        paragraph_mean and paragraph_sigma.
        :param float paragraph_mean:    Override the paragraph mean value.
        :param float paragraph_sigma:   Override the paragraph sigma value.
        :returns:                       A tuple containing number of sentences,
                                        number of words, and the paragraph
                                        text.
        :rtype:                         tuple(int, int, str or unicode)
        """

        # The length of the paragraph is a normally distributed random
        # variable.
        paragraph_mean = args.get('paragraph_mean', self.paragraph_mean)
        paragraph_sigma = args.get('paragraph_sigma', self.paragraph_sigma)
        paragraph_len = int(1 + ceil(abs(normalvariate(paragraph_mean,
                                                       paragraph_sigma))))
        paragraph_len = args.get('paragraph_len', paragraph_len)

        words = 0
        paragraph = []

        generator = self.generate_sentences(paragraph_len, **args)
        for word_count, sentence in generator:
            words += word_count
            paragraph.append(sentence)

        # Form the paragraph into a string.
        return (paragraph_len, words, ' '.join(paragraph))

    def generate_paragraphs(self, amount, **args):
        """Generator method that yields paragraphs, of random length.

        Also accepts the same arguments as :py:meth:`generate_paragraph`.

        :param int amount:              The amount of paragraphs to generate.
        :retruns:                       A generator of specified amount tuples.
                                        as per :py:meth:`generate_paragraph`
        :rtype:                         generator
        """
        yield self.generate_paragraph(**args)
        args['incipit'] = False
        need, more_paragraphs = next, iter(range(amount - 1))
        while need(more_paragraphs, False) is not False:
            yield self.generate_paragraph(**args)
