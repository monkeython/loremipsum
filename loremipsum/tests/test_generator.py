from loremipsum import generator
from loremipsum import samples

import unittest


try:
    unicode_str = __builtins__.get('unicode')
except AttributeError:
    unicode_str = str


class TestSample(unittest.TestCase):
    """Sample TestCase."""

    @classmethod
    def setUpClass(class_):
        """Setup a loremipsum generator to use in tests."""
        class_._s = samples.DEFAULT

    def test_text(self):
        """Test Sample['text'] property."""
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
        self.assertIsInstance(self._s['text'], unicode_str)

    def test_lexicon(self):
        """Test Sample.lexicon property."""
        with self.assertRaises(TypeError):
            generator.Sample(
                text=self._s['text'],
                lexicon='',
                word_delimiters=self._s['word_delimiters'],
                sentence_delimiters=self._s['sentence_delimiters'])
        self.assertIsInstance(self._s['lexicon'], unicode_str)

    def test_word_delimiters(self):
        """Test Sample.word_delimiters property."""
        self.assertIsInstance(self._s['word_delimiters'], unicode_str)

    def test_sentence_delimiters(self):
        """Test Sample.sentence_delimiters property."""
        self.assertIsInstance(self._s['sentence_delimiters'], unicode_str)

    def test_incipit(self):
        """Test Sample.incipit property."""
        self.assertIsInstance(self._s['incipit'], unicode_str)
        self.assertTrue(self._s['text'].startswith(self._s['incipit']))

#    def test_conf(self):
#        """Test Sample.conf context manager."""
#        conf = dict(sentence_mean=0.9,
#                    sentence_sigma=0.9,
#                    paragraph_mean=0.9,
#                    paragraph_sigma=0.9)
#        with self._s.conf(**conf) as other:
#            state = other.state
#            self.assertEqual(state['sentence']['mean'], 0.9)
#            self.assertEqual(state['sentence']['sigma'], 0.9)
#            self.assertEqual(state['paragraph']['mean'], 0.9)
#            self.assertEqual(state['paragraph']['sigma'], 0.9)
#            self.assertIsNot(self._s, other)

#    def test___cmp__(self):
#        """Test Sample.__cmp__ method."""
#        with self._s.conf() as other:
#            self.assertEqual(self._s, other)
#        with self._s.conf(sentence_sigma=0.9) as other:
#            self.assertNotEqual(self._s, other)
