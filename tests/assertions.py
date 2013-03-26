import sys
sys.path.append('./tests/lib')

from testml import TestML
from testml_bridge import TestMLBridge

TestML(
    testml = 'testml/assertions.tml',
    bridge = TestMLBridge,
)
