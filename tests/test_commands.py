import unittest

import sys
sys.path.append('.')

import testml.setup

class TestCommands(unittest.TestCase):
    def test_commands(self):
        self.assertEquals(1, 1)

if __name__ == '__main__':
    unittest.main()
