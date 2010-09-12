#!/usr/bin/env python
"""

Usage:
        make_module yaml-grammar-file

"""
import sys
import pprint
import yaml

def generate_grammar(yaml_file):
    grammar = yaml.load(file(sys.argv[1]))
    data = pprint.pformat(grammar, indent=2)

    print """\
\"\"\"
Generated TestML Grammar
\"\"\"

import pegex.grammar

class Grammar(pegex.grammar.Grammar):
    def __init__(self, receiver=None):
        pegex.grammar.Grammar.__init__(self, receiver=receiver)
        self.grammar = {}
        self.grammar.update(
%(data)s
)
""" % locals(),

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception(__doc__)
    grammar_file = sys.argv[1]
    generate_grammar(grammar_file)
