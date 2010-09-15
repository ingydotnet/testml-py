"""\
TestML debugging module.
"""

import os, sys
sys.path.insert(0, '../pegex-py/')

def XXX(o):
    import yaml
    print yaml.dump(o, default_flow_style=False)
    os.execlp('true')

