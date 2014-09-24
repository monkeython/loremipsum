from loremipsum import functions
from loremipsum import generator

import sys
import types
import unittest


unicode_str = sys.version_info[0] == 3 and str or unicode


class TestFunctions(unittest.TestCase):
    """Functions testcase."""

    def test_generate_sentence(self):
        """Test functions.generate_sentence function."""
        words, sentence = functions.generate_sentence(incipit=True)
        self.assertEqual(words, len(list(generator._words_finditer(sentence))))
        incipit_len = min(len(sentence), len(functions._LOREMIPSUM.incipit))
        incipit_len -= 1
        self.assertEqual(sentence[:incipit_len],
                         functions._LOREMIPSUM.incipit[:incipit_len])

        words, sentence = functions.generate_sentence(sentence_len=5)
        self.assertEqual(5, words)
        self.assertEqual(5, len(list(generator._words_finditer(sentence))))

    def test_generate_sentences(self):
        """Test functions.generate_sentence function."""
        gen = functions.generate_sentences(100, sentence_mean=0.1,
                                           sentence_sigma=0.1)
        self.assertIsInstance(gen, types.GeneratorType)
        sentences = list(gen)
        self.assertEqual(len(sentences), 100)
        for sentence_len, sentences in sentences:
            self.assertEqual(sentence_len, 2)

    def test_generate_paragraph(self):
        """Test functions.generate_paragraph function."""
        sentences, words, text = functions.generate_paragraph()
        len_ = len(list(generator._sentences_finditer(functions._LOREMIPSUM,
                                                      text)))
        self.assertEqual(sentences, len_)
        self.assertEqual(words, len(list(generator._words_finditer(text))))

        sentences, words, text = functions.generate_paragraph(paragraph_len=5)
        self.assertEqual(sentences, 5)

    def test_generate_paragraphs(self):
        """Test functions.generate_paragraphs function."""
        gen = functions.generate_paragraphs(100, paragraph_mean=0.1,
                                            paragraph_sigma=0.1)
        self.assertIsInstance(gen, types.GeneratorType)
        paragraphs = list(gen)
        self.assertEqual(len(paragraphs), 100)
        for paragraph_len, words, text in paragraphs:
            self.assertEqual(paragraph_len, 2)

    def test_get_word(self):
        """Test functions.get_word function."""
        self.assertEqual(len(functions.get_word(5)), 5)
        self.assertIsNone(functions.get_word(100))

    def test_get_words(self):
        """Test functions.get_words function."""
        gen = functions.get_words(100)
        self.assertIsInstance(gen, types.GeneratorType)
        gen = list(gen)
        self.assertEqual(len(gen), 100)
        self.assertTrue(reduce(lambda a, b: a != b, [len(g) for g in gen]))

        gen = functions.get_words(10, 5)
        self.assertTrue(all([len(g) == 5 for g in gen]))

    def test_get_sentence(self):
        """Test functions.get_sentence function."""
        self.assertIsInstance(functions.get_sentence(), unicode_str)

    def test_get_sentences(self):
        """Test functions.get_sentences function."""
        l = functions.get_sentences(5)
        self.assertIsInstance(l, list)
        self.assertEqual(len(l), 5)

    def test_get_paragraph(self):
        """Test functions.get_paragraph function."""
        self.assertIsInstance(functions.get_paragraph(), unicode_str)

    def test_get_paragraphs(self):
        """Test functions.get_paragraphs function."""
        l = functions.get_paragraphs(3)
        self.assertIsInstance(l, list)
        self.assertEqual(len(l), 3)
