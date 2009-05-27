from testml.runner import Runner as SuperRunner

class Runner(SuperRunner):
    """
    A runner implementation for when we are using py.test
    as the test harness.
    """

    def setup(self):
        pass

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
