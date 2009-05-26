from testml.bridge import Bridge as SuperBridge, TRANSFORM_CLASSES

TRANSFORM_CLASSES.append('bridge')

def testml_my_thing(self, args):
    return ' - '.join(self.value.rstrip('\n').split('\n'))

class Bridge(SuperBridge):
    pass
