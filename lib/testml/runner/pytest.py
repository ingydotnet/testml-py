from testml.runner import Runner as SuperRunner

class Runner(SuperRunner):
    """
    A runner implementation for when we are using py.test
    as the test harness.
    """

    def init_bridge(self):
        return self.bridge()

    def title(self):
        if self.doc.meta.data['Title']:
            print "=== %s ===" % self.doc.meta.data['Title']

    def do_test(self, operator, left, right, label=None):
        def test():
            try:
                assert left.value == right.value, label
            except AssertionError:
                print "\nGot:  '%s'" % left.value
                print "Want: '%s'" % right.value
            finally:
                assert left.value == right.value, label

        return test

# XXX Use an importable dict for global settings. Would be nice to do this
# even cleaner.
TESTML = {
    'document': None,
    'stream': None,
    'bridge': None,
    'base': None,
}
def test():
    base = TESTML['base']
    if base and base.find('/') >= 0:
        base = base[0:base.rfind('/')]
    document = TESTML['document']
    stream = TESTML['stream']
    bridge = TESTML['bridge']
    if not bridge:
        from bridge import Bridge
        bridge = Bridge

    for test in Runner(
        document=document,
        stream=stream,
        bridge=bridge,
        base=base,
    ).run(): yield test
