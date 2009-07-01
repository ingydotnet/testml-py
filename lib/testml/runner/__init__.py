
from testml.document import Document, Builder
from testml.parser import Parser

import os

class RunnerException(Exception):
    pass

class Context(object):
    def __init__(self, document=None, block=None, value=None):
        self.document = document
        self.block = block
        self.point = None
        self.value = value
        self.error = None

class Runner(object):
    def __init__(self, document=None, bridge=None):
        self.document = document
        # self.base = document.replace(...)
        self.bridge = bridge
        self.doc = self.parse()
        self.Bridge = self.init_bridge()

    def init_bridge(self):
        """Initialize the Bridge Class. Will throw if it can't import."""
        return self.bridge()


    def run(self):
        self.setup()
        self.title()
        self.plan_begin()

        count = 0
        for statement in self.doc.tests.statements:
            blocks = self.select_blocks(statement.points)

            for block in blocks:
                count += 1
                left = self.evaluate_expression(statement.left_expression[0], block)
                if statement.right_expression:
                    right = self.evaluate_expression(statement.right_expression[0], block)
                    yield '%s:%s:%s' % (self.doc.meta.data['Title'], block.label, count), self.do_test('EQ', left, right, block.label)

        self.plan_end()

    def select_blocks(self, requested_points):
        blocks = []

        for block in self.doc.data.blocks:
            if block.points.has_key('SKIP'):
                continue
            if block.points.has_key('LAST'):
                break
            try:
                for point in requested_points:
                    if not block.points[point]:
                        raise StopIteration
            except StopIteration:
                continue
            if block.points.has_key('ONLY'):
                blocks = [block]
                break
            blocks.append(block)

        return blocks

    def plan_begin(self):
        pass

    def plan_end(self):
        pass

    def evaluate_expression(self, expression, block):
        context = Context(document=self.doc, block=block, value=None)
        
        for transform in expression.transforms:
            if (context.error and transform.name != 'Catch'):
                continue
            function = self.Bridge._get_transform_function(transform.name)
            try:
                context.value = function(context, transform.args)
            except Exception, e:
                context.error = e
        if context.error:
            raise context.error
        return context

    def parse(self):
        """parse the document"""
        parser = Parser(receiver=Builder(), start_token='document')
        parser.open(self.document)
        parser.parse()
        self.parse_data(parser.receiver)
        return parser.receiver.document

    def parse_data(self, builder):
        document = builder.document
        for file in document.meta.data['Data']:
            parser = Parser(receiver=Builder(), start_token='data')
            if file == '_':
                parser.stream = builder.inline_data
            else:
                parser.open(os.path.join(self.base, file))
            parser.parse()
            document.data.blocks.extend(parser.receiver.blocks)

    def title(self):
        raise RunnerException("Don't use %s directly. Use a subclass" % self.__class__)

    def setup(self):
        raise RunnerException("Don't use %s directly. Use a subclass" % self.__class__)

    def do_test(self, operator, left, right, lable=None):
        raise RunnerException("Don't use %s directly. Use a subclass" % self.__class__)
