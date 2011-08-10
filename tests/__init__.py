from unittest import defaultTestLoader, TestSuite
import test_loremipsum

suite = TestSuite()
suite.addTest(defaultTestLoader.loadTestsFromModule(test_loremipsum))
