import sys
sys.path.append('./test/lib')

from testml import TestML
from testml_bridge import TestMLBridge
from testml.compiler.lite import Lite as Compiler

TestML(
    testml = 'testml/exceptions.tml',
    bridge = TestMLBridge,
    compiler = Compiler,
)
