def get():
    info = {}
    info.update(
{ 'author': 'Ingy dot Net',
  'author_email': 'ingy@ingy.net',
  'classifiers': [ 'Development Status :: 2 - Pre-Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python',
                   'Topic :: Software Development',
                   'Topic :: System :: Software Distribution'],
  'description': 'TestML -- An Acmeist Unit Testing Framework',
  'install_requires': ['pyyaml'],
  'long_description': 'The Python implementation of TestML.\n',
  'name': 'testml',
  'packages': ['testml', 'testml.parser', 'testml.runner'],
  'scripts': [],
  'url': 'http://www.testml.org/',
  'version': '0.2.0'}
)
    return info
