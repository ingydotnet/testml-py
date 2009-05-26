
def testml_Point(self, name):
    self.point = name
    value = self.block.points[name]
    # XXX whitespace handling missing
    return value

