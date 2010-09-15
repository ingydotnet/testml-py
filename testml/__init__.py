"""\
TestML -- An Acmeist Unit Testing Framework
"""

__version__ = '0.2.0'
__ALL__ = ['TestML', 'test']

import inspect
from testml.XXX import *

from package.unittest import *

class Test():
    def __init__(self):
        self.run = 'unittest'
        self.ran = False
        self.document = None
        self.stream = None
        self.bridge = None
        self.base = None

TestML = Test()

def test():
    if TestML.ran:
        return
    else:
        TestML.ran = True

    base = inspect.stack()[1][1]
    try:
        r = base.rindex('/')
        base = base[0:r]
    except ValueError:
        pass

    TestML.base = base
    XXX(TestML)
