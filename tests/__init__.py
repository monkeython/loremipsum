from unittest import defaultTestLoader, TestSuite
from . import test_generator
from . import test_functions

suite = TestSuite()
suite.addTest(defaultTestLoader.loadTestsFromModule(test_generator))
suite.addTest(defaultTestLoader.loadTestsFromModule(test_functions))
