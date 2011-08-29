from unittest import defaultTestLoader, TestSuite
import test_generator
import test_functions

suite = TestSuite()
suite.addTest(defaultTestLoader.loadTestsFromModule(test_generator))
suite.addTest(defaultTestLoader.loadTestsFromModule(test_functions))
