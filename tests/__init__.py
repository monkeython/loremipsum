import unittest

from tests import test_functions
from tests import test_generator

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_generator))
suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_functions))
