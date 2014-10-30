from loremipsum import generator
from loremipsum import samples

import sys
import unittest


builtins = sys.modules.get('__builtin__', sys.modules.get('builtins'))


class TestSample(unittest.TestCase):
    """Sample TestCase."""

    @classmethod
    def setUpClass(class_):
        """Setup a loremipsum generator to use in tests."""
        class_._s = samples.DEFAULT
        class_._unicode_str = getattr(builtins, 'unicode', str)

    def test_text(self):
        """Test Sample['text'] item."""
        with self.assertRaises(ValueError):
            generator.Sample(
                text=' . , ! ?',
                lexicon=self._s['lexicon'],
                word_delimiters=self._s['word_delimiters'],
                sentence_delimiters=self._s['sentence_delimiters'])
        with self.assertRaises(TypeError):
            generator.Sample(
                text='',
                lexicon=self._s['lexicon'],
                word_delimiters=self._s['word_delimiters'],
                sentence_delimiters=self._s['sentence_delimiters'])
        self.assertIsInstance(self._s['text'], self._unicode_str)

    def test_lexicon(self):
        """Test Sample['lexicon'] item."""
        with self.assertRaises(TypeError):
            generator.Sample(
                text=self._s['text'],
                lexicon='',
                word_delimiters=self._s['word_delimiters'],
                sentence_delimiters=self._s['sentence_delimiters'])
        with self.assertRaises(ValueError):
            generator.Sample(
                text=self._s['text'],
                lexicon='\t',
                word_delimiters=self._s['word_delimiters'],
                sentence_delimiters=self._s['sentence_delimiters'])
        self.assertIsInstance(self._s['lexicon'], self._unicode_str)

    def test_word_delimiters(self):
        """Test Sample['word_delimiters'] item."""
        self.assertIsInstance(self._s['word_delimiters'],
                              self._unicode_str)

    def test_sentence_delimiters(self):
        """Test Sample['sentence_delimiters'] item."""
        self.assertIsInstance(self._s['sentence_delimiters'],
                              self._unicode_str)

    def test_incipit(self):
        """Test Sample['incipit'] item."""
        self.assertIsInstance(self._s['incipit'], self._unicode_str)
        self.assertTrue(self._s['text'].startswith(self._s['incipit']))

    def test_cooked(self):
        """Test Sample.cooked and Sample.row."""
        sample = generator.Sample.cooked(*self._s.row())
        self.assertEqual(hash(sample), hash(self._s))

    def test_thawed(self):
        """Test Sample.cooked and Sample.row."""
        sample = generator.Sample.thawed(self._s.frozen())
        self.assertEqual(hash(sample), hash(self._s))

    def test_duplicated(self):
        """Test Sample.cooked and Sample.row."""
        sample = generator.Sample.duplicated(self._s)
        self.assertEqual(hash(sample), hash(self._s))

    def test___iter__(self):
        """Test Sample.__iter__."""
        for key in self._s:
            self.assertIn(key, self._s._s)

    def test___eq__(self):
        """Test Sample.__eq__."""
        self.assertEqual(self._s, samples.DEFAULT)


class TestGenerator(unittest.TestCase):
    """Sample TestCase."""

    @classmethod
    def setUpClass(class_):
        """Setup a loremipsum generator to use in tests."""
        class_._g = generator.Generator(samples.DEFAULT)

    def test_default(self):
        """Test Generator.default context manager."""
        conf = dict(sentence_mean=0.9,
                    sentence_sigma=0.9,
                    paragraph_mean=0.9,
                    paragraph_sigma=0.9)
        with self._g.default(**conf) as other:
            self.assertEqual(other.sample['sentence_mean'], 0.9)
            self.assertEqual(other.sample['sentence_sigma'], 0.9)
            self.assertEqual(other.sample['paragraph_mean'], 0.9)
            self.assertEqual(other.sample['paragraph_sigma'], 0.9)
            self.assertIsNot(self._g, other)
            self.assertIsNot(self._g.sample, other.sample)
            self.assertNotEqual(self._g.sample, other.sample)

    def test_sample(self):
        """Test Generator.sample property get/set."""
        self.maxDiff = None
        with self._g.default(sentence_mean=0.9) as other:
            row = samples.DEFAULT.row()
            other.sample = row
            self.assertEqual(other.sample.row(), row)

            frozen = samples.DEFAULT.frozen()
            other.sample = frozen
            self.assertEqual(other.sample.frozen(), frozen)

            copy = samples.DEFAULT.copy()
            self.assertIsInstance(copy, dict)
            other.sample = copy
            self.assertDictEqual(other.sample.copy(), copy)

            other.sample = samples.DEFAULT
            self.assertIs(other.sample, samples.DEFAULT)
            with self.assertRaises(ValueError):
                other.sample = list(row)
