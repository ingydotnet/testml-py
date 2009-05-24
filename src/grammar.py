import yaml

import sys

file = sys.argv[1]

fh = open(file)

data = yaml.load(fh)

print """\
class Grammar(object):
    def grammar(self):
        return """,
print data
