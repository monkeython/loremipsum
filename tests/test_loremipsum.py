import loremipsum
import unittest
from types import GeneratorType

class TestGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = loremipsum.Generator()

    def test_sample(self):
        with self.assertRaises(loremipsum.SampleError):
            self.generator.sample = ' . , ! ? '
        with self.assertRaises(loremipsum.SampleError):
            self.generator.sample = ''
        sample = self.generator.sample
        self.assertTrue(isinstance(sample, str))

    def test_dictionary(self):
        with self.assertRaises(loremipsum.DictionaryError):
            self.generator.dictionary = []
        dictionary = self.generator.dictionary
        self.assertTrue(isinstance(dictionary, dict))

    def _test_sigma_mean(self, attr):
        self.assertTrue(isinstance(getattr(self.generator, attr), float))
        with self.assertRaises(ValueError):
            setattr(self.generator, attr, -1)

    def test_sentence_sigma(self):
        self._test_sigma_mean('sentence_sigma')

    def test_sentence_mean(self):
        self._test_sigma_mean('sentence_mean')

    def test_paragraph_sigma(self):
        self._test_sigma_mean('paragraph_sigma')

    def test_paragraph_mean(self):
        self._test_sigma_mean('paragraph_mean')

    def _test_generated(self, generated, start_with_lorem=False):
        self.assertEqual(len(generated), 3)
        self.assertTrue(isinstance(generated, tuple))
        sentences, words, text = generated
        self.assertTrue(isinstance(sentences, int))
        self.assertTrue(isinstance(words, int))
        self.assertTrue(isinstance(text, str))
        self.assertEqual(text.startswith('Lorem ipsum'), start_with_lorem)

    def _test_generators(self, method, start_with_lorem=False):
        generator = method(3, start_with_lorem)
        self.assertTrue(isinstance(generator, GeneratorType))
        self._test_generated(generator.next(), start_with_lorem)
        generated = 1
        for each in generator:
            self._test_generated(each)
            generated +=1
        self.assertEqual(generated, 3)

    def test_generate_sentence(self):
        self._test_generated(self.generator.generate_sentence(True), True)
        self._test_generated(self.generator.generate_sentence(False), False)

    def test_generate_sentences(self):
        self._test_generators(self.generator.generate_sentences, True)
        self._test_generators(self.generator.generate_sentences, False)

    def test_generate_paragraph(self):
        self._test_generated(self.generator.generate_paragraph(True), True)
        self._test_generated(self.generator.generate_paragraph(False), False)

    def test_generate_paragraphs(self):
        self._test_generators(self.generator.generate_paragraphs, True)
        self._test_generators(self.generator.generate_paragraphs, False)

class TestLoremIpsum(unittest.TestCase):

    def _test_text(self, text, start_with_lorem=False):
        self.assertTrue(isinstance(text, str))
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
