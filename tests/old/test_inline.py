import sys; sys.path.insert(0, 'lib')
from testml.runner.pytest import TESTML, test
TESTML['stream'] = """\
%TestML: 1.0
%Title: Ingy's Test
%Plan: 4

$foo == $bar;
$bar == $foo;

=== Foo for thought
--- foo: O HAI
--- bar: O HAI

=== Bar the door
--- bar
O
HAI
--- foo
O
HAI
"""
