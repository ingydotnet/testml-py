import sys; sys.path.insert(0, 'lib')

from testml.runner.pytest import Runner
from bridge import Bridge

def test():
    for test in Runner('tests/testml/no-data.tml', Bridge).run(): yield test
