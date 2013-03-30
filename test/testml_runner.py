import sys
sys.path.insert(0, '.')
sys.path.insert(0, './test')

import unittest
import testml
import testml.compiler
import testml.compiler.pegex
import testml.compiler.lite
import testml_bridge

import re
import glob

class TestMLTestCase(unittest.TestCase):
    def run_testml_file(self, file_, compiler=testml.compiler.pegex.Pegex):
        testml.TestML(
            testml = file_,
            bridge = testml_bridge.TestMLBridge,
            compiler = compiler,
        ).run(self)

files = glob.glob('test/testml/*.tml')
files.sort()
files = map(lambda f: f.replace('test/', ''), files)
files = filter(lambda f: not(re.search(r'external[12]', f)), files)
for file_ in files:
    method_name = 'test_' + re.sub(r'\W', '_', file_)
    method_name = re.sub(r'_tml$', '', method_name)
    def method(self, file_ = file_):
        self.run_testml_file(file_)
    setattr(TestMLTestCase, method_name, method)

files = """
test/arguments.tml
test/basic.tml
test/exceptions.tml
test/semicolons.tml
""".strip().split()
for file_ in files:
    method_name = 'test_lite_' + re.sub(r'\W', '_', file_)
    method_name = re.sub(r'_tml$', '', method_name)
    def method(self, file_ = file_):
        self.run_testml_file(file_)
    setattr(TestMLTestCase, method_name, method)

if __name__ == '__main__':
    unittest.main()

