import loremipsum
import unittest
import sys

if sys.version_info[0] == 3:
    unicode = str


class TestLoremIpsum(unittest.TestCase):

    def _test_text(self, text, start_with_lorem=False):
        self.assertTrue(isinstance(text, unicode))
        self.assertEqual(text.startswith('Lorem ipsum'), start_with_lorem)

    def _test_get_function(self, function):
        self._test_text(function(True), True)
        self._test_text(function(False), False)

    def _test_iterators_function(self, function):
        iterator = function(3, True)
        self.assertTrue(isinstance(iterator, list))
        self.assertEqual(len(iterator), 3)
        self._test_text(iterator[0], True)
        for each in iterator[1:]:
            self._test_text(each, False)
        iterator = function(3, False)
        self.assertTrue(isinstance(iterator, list))
        self.assertEqual(len(iterator), 3)
        for each in iterator:
            self._test_text(each, False)

    def test_get_sentence(self):
        self._test_get_function(loremipsum.get_sentence)

    def test_get_sentences(self):
        self._test_iterators_function(loremipsum.get_sentences)

    def test_get_paragraph(self):
        self._test_get_function(loremipsum.get_paragraph)

    def test_get_paragraphs(self):
        self._test_iterators_function(loremipsum.get_paragraphs)
