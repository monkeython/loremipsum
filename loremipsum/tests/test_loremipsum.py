import loremipsum

import types
import unittest


try:
    unicode_str = __builtins__.get('unicode')
except AttributeError:
    unicode_str = str


class TestLoremipsum(unittest.TestCase):
    """Functions testcase."""

    @classmethod
    def setUpClass(class_):
        """Setup default sample."""
        class_._s = loremipsum.samples.DEFAULT

    def test_generate_sentence(self):
        """Test loremipsum.generate_sentence function."""
        words, sentence = loremipsum.generate_sentence(incipit=True)
        self.assertEqual(words, len(list(self._s._find_words(sentence))))
        min_len = min(len(sentence), len(self._s['incipit'])) - 1
        self.assertEqual(sentence[:min_len], self._s['incipit'][:min_len])
        words, sentence = loremipsum.generate_sentence(sentence_len=5)
        self.assertEqual(5, words)
        self.assertEqual(5, len(list(self._s._find_words(sentence))))

    def test_generate_sentences(self):
        """Test loremipsum.generate_sentences function."""
        gen = loremipsum.generate_sentences(
            100, incipit=True, sentence_mean=0.1, sentence_sigma=0.1)
        self.assertIsInstance(gen, types.GeneratorType)
        sentences = list(gen)
        self.assertEqual(len(sentences), 100)
        for sentence_len, sentences in sentences:
            self.assertEqual(sentence_len, 2)

        for words, sentences in loremipsum.generate_sentences(100):
            self.assertEqual(words, len(list(self._s._find_words(sentences))))

    def test_generate_paragraph(self):
        """Test loremipsum.generate_paragraph function."""
        sentences, words, text = loremipsum.generate_paragraph()
        self.assertEqual(sentences, len(list(self._s._find_sentences(text))))
        self.assertEqual(words, len(list(self._s._find_words(text))))
        sentences, words, text = loremipsum.generate_paragraph(paragraph_len=5)
        self.assertEqual(sentences, 5)

    def test_generate_paragraphs(self):
        """Test loremipsum.generate_paragraphs function."""
        gen = loremipsum.generate_paragraphs(
            100, incipit=True, paragraph_mean=0.1, paragraph_sigma=0.1)
        self.assertIsInstance(gen, types.GeneratorType)
        paragraphs = list(gen)
        self.assertEqual(len(paragraphs), 100)
        for paragraph_len, words, text in paragraphs:
            self.assertEqual(paragraph_len, 2)

    def test_get_word(self):
        """Test loremipsum.get_word function."""
        self.assertEqual(len(loremipsum.get_word(5)), 5)
        self.assertIsNone(loremipsum.get_word(100))

    def test_get_words(self):
        """Test loremipsum.get_words function."""
        gen = loremipsum.get_words(100)
        self.assertIsInstance(gen, types.GeneratorType)
        gen = list(gen)
        self.assertEqual(len(gen), 100)
        lens = [len(word) for word in gen]
        equal = True
        previous = lens[0]
        for len_ in lens[1:]:
            equal = equal and previous == len_
            previous = len_

        self.assertFalse(equal)
        gen = loremipsum.get_words(10, 5)
        self.assertTrue(all([len(g) == 5 for g in gen]))

    def test_get_sentence(self):
        """Test loremipsum.get_sentence function."""
        self.assertIsInstance(loremipsum.get_sentence(), unicode_str)

    def test_get_sentences(self):
        """Test loremipsum.get_sentences function."""
        l = loremipsum.get_sentences(5)
        self.assertIsInstance(l, types.GeneratorType)
        self.assertEqual(len(list(l)), 5)

    def test_get_paragraph(self):
        """Test loremipsum.get_paragraph function."""
        self.assertIsInstance(loremipsum.get_paragraph(), unicode_str)

    def test_get_paragraphs(self):
        """Test loremipsum.get_paragraphs function."""
        l = loremipsum.get_paragraphs(3)
        self.assertIsInstance(l, types.GeneratorType)
        self.assertEqual(len(list(l)), 3)
