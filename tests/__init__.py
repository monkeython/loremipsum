import unittest

import test_functions
import test_generator

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_generator))
suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_functions))
