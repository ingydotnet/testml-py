import sys
sys.path.append('./test/lib')

from testml import TestML
from testml_bridge import TestMLBridge

TestML(
    testml = 'testml/function.tml',
    bridge = TestMLBridge,
)
