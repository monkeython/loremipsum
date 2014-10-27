import types
import unittest

import loremipsum


try:
    unicode_str = __builtins__.get('unicode')
except AttributeError:
    unicode_str = str


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
        registered = self._package.registered()
        self.assertIsInstance(registered, dict)
        self.assertIn(self._plug_name, registered)
        self.assertEqual(registered, loremipsum._PLUGS[self._package.__name__])
        self.assertIsNot(registered, loremipsum._PLUGS[self._package.__name__])

    def test_DEFAULT(self):
        """Test default package plug."""
        classes = (types.ModuleType, loremipsum.generator.Sample)
        self.assertIs(self._package.DEFAULT, self._package.get(self._DEFAULT))
        self.assertIsInstance(self._package.DEFAULT, classes)
