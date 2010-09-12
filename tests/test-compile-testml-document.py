from package.unittest import *

class TestCompile(TestCase):
    def test_compile(self):
        import testml
        import testml.grammar

        self.assertTrue(True, 'testml modules imported cleanly')

if __name__ == '__main__':
    main()
