import re

def Point(self, args):
    name = args[0]
    self.point = name
    value = self.block.points[name]
    value = re.sub(r'\n+\Z', '\n', value, 1)
    if value == '\n':
        value = ''
    return value

def Catch(self, args):
    if not self.error:
        raise Exception, "Catch called but no TestML error found"
    error = self.error
    self.error = None
    return error

def String(self, args=[]):
    if self.value:
        return self.value
    if args[0]:
        try:
            return args[0].value
        except Exception:
            return args[0]
    else:
        raise Exception, "String transform called, but no string available"

def List(self, args):
    return self.value.rstrip('\n').split('\n')

def Join(self, args):
    join_string = args[0]
    if not join_string:
        join_string = ''
    return join_string.join(self.value)

def Reverse(self, args):
    self.value.reverse()
    return self.value

def Item(self, args):
    list = self.value
    list.append('')
    return '\n'.join(list)

def Sort(self, args):
    self.value.sort()
    return self.value
