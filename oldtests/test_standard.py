import sys; sys.path.insert(0, 'lib')
from testml.runner.pytest import TESTML, test
TESTML['stream'] = """\
%TestML: 1.0

$foo.Chomp() == $bar;

=== Test
--- foo
Hello
--- bar: Hello
"""
