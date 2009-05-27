import re
from testml.bridge import Bridge as SuperBridge, TRANSFORM_CLASSES

TRANSFORM_CLASSES.append('bridge')

def testml_my_thing(self, args):
    return ' - '.join(self.value.rstrip('\n').split('\n'))

def testml_parse_testml(self, args):
    from testml.parser import Parser
    from testml.document import Builder
    parser = Parser(
        receiver=Builder(),
        start_token='document'
    )
    parser.stream = self.value
    parser.parse()
    

def testml_msg(self, args):
    value = str(self.value)
    match = re.match(r'msg: (.*)', value)
    if match:
        return match.group(1)
    else:
        return value

class Bridge(SuperBridge):
    pass
