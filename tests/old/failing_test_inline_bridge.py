import sys; sys.path.insert(0, 'lib')
from testml.runner.pytest import TESTML, test
TESTML['stream'] = """\
%TestML: 1.0

$foo.test_upper() == $bar;

=== Foo for thought
--- foo: o hai
--- bar: O HAI

=== Bar the door
--- foo
o
Hai
--- bar
O
HAI
"""

from testml.bridge import Bridge as Super, TRANSFORM_CLASSES
TRANSFORM_CLASSES.append(__file__)
class Bridge1(Super):
    def test_upper(string):
        return string.upper()

TESTML['bridge'] = Bridge1
