import unittest
import testml.runtime

# class TestMLTestCase(unittest.TestCase):
#     def __init__(self, testml_case):
#         self.testml_case = testml_case
#         super(TestMLTestCase, self).__init__()
# 
#     def runTest(self):
#         self.testml_case.run_run()

class Unit(testml.runtime.Runtime):
    def run_run(self):
        #super(Unit, self)
        self.run2()

    def run(self, testcase):
        self.testunit_testcase = testcase

    def assert_EQ(self, got, want):
        self.testunit_testcase.assertEqual(got, want)
