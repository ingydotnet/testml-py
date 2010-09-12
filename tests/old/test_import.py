from package.unittest import *

class TestImport(TestCase):
    def test_import(self):
        import testml
        import testml.grammar

        self.assertTrue(True, 'testml modules imported cleanly')

if __name__ == '__main__':
    main()
