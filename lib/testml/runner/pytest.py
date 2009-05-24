from testml.runner import Runner as SuperRunner

class Runner(SuperRunner):
    """
    A runner implementation for when we are using py.test
    as the test harness.
    """

    def setup(self):
        pass

    def title(self):
        print "=== %s ===" % self.doc.meta.data['Title']

    def do_test(self, operator, left, right, label=None):
        def test():
            assert left == right, label
        yield test
