__version__ = '0.0.2'

from xxx import XXX

class TestML:
    def __init__(self,
        testml=None,
        runtime=None,
        bridge=None,
        library=None,
        compiler=None,
    ):
        self.testml=testml
        self.runtime=runtime
        self.bridge=bridge
        self.library=library
        self.compiler=compiler
        self.base='tests'

    def run(self, testcase):
        self.set_default_classes()
        self.runtime(
            compiler=self.compiler,
            bridge=self.bridge,
            library=self.library,
            testml=self.testml,
            base=self.base,
        ).run(testcase)

    def set_default_classes(self):
        if not self.runtime:
            from testml.runtime.unit import Unit
            self.runtime = Unit
        if not self.compiler:
            from testml.compiler.pegex import Pegex
            self.compiler = Pegex
        if not self.bridge:
            from testml.bridge import Bridge
            self.bridge = Bridge
        if not self.library:
            from testml.library.standard import Standard
            from testml.library.debug import Debug
            self.library = [
                Standard,
                Debug,
            ]
