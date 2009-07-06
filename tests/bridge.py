import re
from testml.bridge import Bridge as SuperBridge, TRANSFORM_CLASSES

TRANSFORM_CLASSES.append('bridge')

def my_thing(self, args):
    return ' - '.join(self.value.rstrip('\n').split('\n'))

def parse_testml(self, args):
    from testml.parser import Parser
    from testml.document import Builder
    parser = Parser(
        receiver=Builder(),
        start_token='document'
    )
    parser.stream = self.value
    parser.parse()
    

def msg(self, args):
    value = str(self.value)
    match = re.match(r'msg: (.*)', value)
    if match:
        return match.group(1)
    else:
        return value

def combine(self, args):
    suffix = args[0].value
    return self.value + ' ' + suffix

class Bridge(SuperBridge):
    pass
