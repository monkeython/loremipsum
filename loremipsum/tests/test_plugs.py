import loremipsum
from loremipsum.tests import testcases

import unittest


class TestSamplesPlugs(testcases.TestPackagesPlugs):
    """Test the generators plugs."""

    @classmethod
    def setUpClass(class_):
        """Setup package and plug name for the tests."""
        class_._package = loremipsum.samples
        class_._plug_name = 'loremipsum'
        class_._DEFAULT = 'loremipsum'


class TestSerializationSchemesPlugs(testcases.TestPackagesPlugs):
    """Test the serialization mediums plugs."""

    @classmethod
    def setUpClass(class_):
        """Setup package and plug name for the tests."""
        class_._package = loremipsum.serialization.schemes
        class_._plug_name = 'file'
        class_._DEFAULT = 'file'


class TestSerializationContentTypesPlugs(testcases.TestPackagesPlugs):
    """Test the serialization protocols plugs."""

    @classmethod
    def setUpClass(class_):
        """Setup package and plug name for the tests."""
        class_._package = loremipsum.serialization.content_types
        class_._plug_name = 'application_json'
        class_._DEFAULT = 'application_json'


class TestSerializationContentEncodingsPlugs(testcases.TestPackagesPlugs):
    """Test the serialization protocols plugs."""

    @classmethod
    def setUpClass(class_):
        """Setup package and plug name for the tests."""
        class_._package = loremipsum.serialization.content_encodings
        class_._plug_name = 'gzip'
        class_._DEFAULT = 'gzip'


class TestPackagePlugsInit(unittest.TestCase):
    """Test the package plugs initialization."""

    def test_setup(self):
        """Test the initialization function."""
        plugs_testpackage = loremipsum.tests.plugs_testpackage
        loremipsum.plugs.setup(plugs_testpackage)
        for function in ['get', 'set_default', 'registered']:
            self.assertIsNotNone(getattr(plugs_testpackage, function, None))

        self.assertIsNone(plugs_testpackage.DEFAULT)
        registered = plugs_testpackage.registered()
        self.assertIsInstance(registered, dict)
        self.assertTrue(registered)
