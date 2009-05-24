
import sys
sys.path.insert(0, 'lib')

import py.test

from testml.runner import Runner, RunnerException
from bridge import Bridge

def test_subclass_only():
    runner = Runner('tests/testml/basic.tml', Bridge)
    py.test.raises(RunnerException, 'runner.setup()')

