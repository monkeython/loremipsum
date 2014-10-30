import unittest

from loremipsum.tests import plugs_testpackage
from loremipsum.tests import test_generator
from loremipsum.tests import test_loremipsum
from loremipsum.tests import test_plugs
from loremipsum.tests import test_serialization

__all__ = [
    'plugs_testpackage',
    'test_generator',
    'test_loremipsum',
    'test_plugs']

suite = unittest.TestSuite()
loader = unittest.defaultTestLoader
suite.addTest(loader.loadTestsFromModule(test_generator))
suite.addTest(loader.loadTestsFromModule(test_loremipsum))
suite.addTest(loader.loadTestsFromModule(test_plugs))
suite.addTest(loader.loadTestsFromModule(test_serialization))
