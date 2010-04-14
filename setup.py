#!/usr/bin/env python
# coding=utf-8

import os
import sys
import codecs
import glob

from distutils.core import setup, Command

import testml


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

        for test in glob.glob(self.test_dir + '/*.py'):
            name = test[test.index('/') + 1: test.rindex('.')]
            module = __import__(name)
            module.testml.test.main(module=module, argv=[''])


class DevTest(Test):
    test_dir = 'dev-tests'


if __name__ == '__main__':
    packages = []
    for t in os.walk('testml'):
        packages.append(t[0].replace('/', '.'))

    setup(
        name='testml',
        version=testml.__version__,

        description='An Acmeist Test Framework',
        long_description = codecs.open(
            os.path.join(
                os.path.dirname(__file__),
                'README.rst'
            ),
            'r',
            'utf-8'
        ).read(),

        # See: http://pypi.python.org/pypi?:action=list_classifiers
        classifiers = [
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Topic :: Software Development',
            'Topic :: System :: Software Distribution',
            'Topic :: Utilities',
        ],

        author='Ingy dot Net',
        author_email='ingy@ingy.net',
        license='Simplified BSD License',
        url='http://www.testml.org/',

        packages=packages,

        cmdclass={
            'test': Test,
            'devtest': DevTest,
        },
    )
