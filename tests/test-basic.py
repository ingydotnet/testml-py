import sys;
sys.path.insert(0, '.')
sys.path.insert(0, 'tests')
from testml import *
TestML.runner = 'testml.runtime.unittest'
TestML.document = 'testml/basic.tml'
TestML.bridge = 'bridge'
test()
