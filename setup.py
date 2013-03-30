import os, sys, glob
from distutils.core import Command

try:
    from setuptools import setup
    has_setuptools = True
except ImportError, err:
    try:
        from distutils.core import setup
    except ImportError, err:
        raise err

class Test(Command):
    user_options = []
    test_dir = 'tests'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        build_cmd = self.get_finalized_command('build')
        build_cmd.run()
        sys.path.insert(0, build_cmd.build_lib)
        sys.path.insert(0, self.test_dir)
        def exit(code):
            pass
        sys.exit = exit

        for test in glob.glob(self.test_dir + '/test*.py'):
            name = test[test.index('/') + 1: test.rindex('.')]
            module = __import__(name)
            if module.__dict__.get('unittest'):
                module.unittest.main(module=module, argv=[''])

args = {
    'author': 'Ingy dot Net',
    'author_email': 'ingy@ingy.net',
    'cmdclass': {
        'test': Test,
    },
    'description': "C'Dent - A Portable Module Programming Language",
    'install_requires': ['pyyaml'],
    'name': 'testml',
#     'packages': [
#         'testml',
#         'testml.compiler',
#         'testml.compiler.pegex',
#         'testml.compiler.lite',
#         'testml.library',
#         'testml.library.debug',
#         'testml.library.standard',
#         'testml.runtime',
#         'testml.runtime.unit',
#         'testml.setup',
#     ],
    'url': 'http://www.testml.org/',
    'version': '0.0.1',
}
setup(**args)
