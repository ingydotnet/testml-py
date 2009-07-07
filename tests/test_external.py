import sys; sys.path.insert(0, 'lib')
from testml.runner.pytest import TESTML, test
TESTML['base'] = __file__
TESTML['stream'] = """\
%TestML: 2.0
%Plan: 4
%Data: external2.tml
%Data: external1.tml

$foo == $bar;
"""
