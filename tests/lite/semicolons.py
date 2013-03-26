import sys
sys.path.append('./tests/lib')

from testml import TestML
from testml_bridge import TestMLBridge
from testml.compiler.lite import Lite as Compiler

TestML(
    testml = 'testml/semicolons.tml',
    bridge = TestMLBridge,
    compiler = Compiler,
)
