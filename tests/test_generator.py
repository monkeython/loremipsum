from loremipsum import functions
from loremipsum import generator

import sys
import types
import unittest


unicode_str = sys.version_info[0] == 3 and str or unicode


class TestGenerator(unittest.TestCase):
    """Generator TestCase."""

    def setUp(self):
        """Setup a loremipsum generator to use in tests."""
        self.loremipsum = functions._LOREMIPSUM

    def test_sample(self):
        """Test Generator.sample property."""
        with self.assertRaises(ValueError):
            generator.Generator(' . , ! ?',
                                functions._LEXICON,
                                functions._WORD_DELIMITERS,
                                functions._SENTENCE_DELIMITERS)
        with self.assertRaises(ValueError):
            generator.Generator('',
                                functions._LEXICON,
                                functions._WORD_DELIMITERS,
                                functions._SENTENCE_DELIMITERS)
        self.assertIsInstance(self.loremipsum.sample, unicode_str)

    def test_lexicon(self):
        """Test Generator.lexicon property."""
        with self.assertRaises(ValueError):
            generator.Generator(functions._SAMPLE,
                                list(),
                                functions._WORD_DELIMITERS,
                                functions._SENTENCE_DELIMITERS)
        lexicon = self.loremipsum.lexicon
        self.assertIsInstance(lexicon, tuple)
        for i in range(len(lexicon)):
            self.assertIsInstance(lexicon[i], unicode_str)

    def test_incipit(self):
        """Test Generator.incipit property."""
        sample, incipit = self.loremipsum.sample, self.loremipsum.incipit
        self.assertIsInstance(incipit, unicode_str)
        self.assertTrue(sample.startswith(incipit))

    def test_generate_word(self):
        """Test Generator.generate_word method."""
        self.assertIsInstance(self.loremipsum.generate_word(), unicode_str)
        self.assertIsNone(self.loremipsum.generate_word(15))
        self.assertTrue(len(self.loremipsum.generate_word(5)), 5)

    def test_generate_words(self):
        """Test Generator.generate_words method."""
        words = self.loremipsum.generate_words(5)
        self.assertIsInstance(words, types.GeneratorType)
        self.assertTrue(len(list(words)), 5)
