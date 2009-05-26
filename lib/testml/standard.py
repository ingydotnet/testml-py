import re

def testml_Point(self, name):
    self.point = name
    value = self.block.points[name]
    value = re.sub(r'\n+\Z', '\n', value, 1)
    if value == '\n':
        value = ''
    return value

def testml_List(self, args):
    return self.value.rstrip('\n').split('\n')

def testml_Join(self, args):
    join_string = args[0]
    if not join_string:
        join_string = ''
    return join_string.join(self.value)

def testml_Reverse(self, args):
    self.value.reverse()
    return self.value

def testml_Item(self, args):
    list = self.value
    list.append('')
    return '\n'.join(list)

def testml_Sort(self, args):
    self.value.sort()
    return self.value
