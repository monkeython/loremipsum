import types
import unittest

import loremipsum


class TestPackagesPlugs(unittest.TestCase):
    """Packages plugs TestCase."""

    def test_get(self):
        """Test package get function."""
        module = self._package.get(self._plug_name)
        Sample = loremipsum.generator.Sample
        self.assertIsInstance(module, (types.ModuleType, Sample))
        # Plug name may be different from module name
        attrs = [getattr(self._package, attr) for attr in dir(self._package)]
        self.assertIn(module, attrs)

    def test_set_default(self):
        """Test package set_default function."""
        module = self._package.get(self._plug_name)
        self._package.set_default(self._plug_name)
        self.assertIs(module, self._package.DEFAULT)

    def test_registered(self):
        """Test package registered function."""
        _REGISTERED = loremipsum.plugs._REGISTERED
        registered = self._package.registered()
        self.assertIsInstance(registered, dict)
        self.assertIn(self._plug_name, registered)
        self.assertEqual(registered, _REGISTERED[self._package.__name__])
        self.assertIsNot(registered, _REGISTERED[self._package.__name__])

    def test_DEFAULT(self):
        """Test default package plug."""
        classes = (types.ModuleType, loremipsum.generator.Sample)
        self.assertIs(self._package.DEFAULT, self._package.get(self._DEFAULT))
        self.assertIsInstance(self._package.DEFAULT, classes)


class TestSerializationScheme(unittest.TestCase):

    def test_dump_load(self):
        """Test dump/load functionss of a serialization scheme module."""
        for url, args in self._urls.items():
            self._dump(url, **args)
            self._load(url, **args)
            self._remove(url, **args)

    def _dump(self, url, **args):
        """Apply the Sample.dump method."""
        self._sample.dump(url, **args)

    def _load(self, url, **args):
        """Apply the Sample.load classmethod."""
        original = self._sample
        self.assertEqual(original, self._sample.load(url, **args))

    def _remove(self, url, **args):
        """Apply the Sample.remove method."""
        self._sample.remove(url)
        with self.assertRaises(self._CannotLoadRemoved):
            self._sample.load(url, **args)
        with self.assertRaises(self._CannotRemoveAgain):
            self._sample.remove(url)


class TestSerializationContentType(unittest.TestCase):

    def test_format_parse(self):
        """Test format/parse functions of a content_types module."""
        frozen = loremipsum.samples.DEFAULT.frozen()
        formatted = self._type.format(frozen)
        parsed = self._type.parse(formatted)
        sample = loremipsum.generator.Sample(**parsed)
        self.assertEqual(loremipsum.samples.DEFAULT, sample)


class TestSerializationContentEncoding(unittest.TestCase):

    def test_encode_decode(self):
        """Test encode/decode functions of a content_encodings module."""
        frozen = (''.join(loremipsum.samples.DEFAULT.row())).encode('UTF-8')
        sample = self._encoding.decode(self._encoding.encode(frozen))
        self.assertEqual(frozen, sample)
