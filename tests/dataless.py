import sys
sys.path.append('./test/lib')

from testml import TestML
from testml_bridge import TestMLBridge

TestML(
    testml = 'testml/dataless.tml',
    bridge = TestMLBridge,
)
