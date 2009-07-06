
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
    def __init__(self, document=None, stream=None, bridge=None):
        self.document = document
        self.stream = stream
        # self.base = document.replace(...)
        self.bridge = bridge
        self.doc = self.parse()
        self.Bridge = self.init_bridge()

    def init_bridge(self):
        # XXX The subclass method should be getting called.
        return self.bridge()
        raise RunnerException("'init_bridge' must me implemented in the subclass")


    def run(self):
        self.title()
        self.plan_begin()

        count = 0
        for statement in self.doc.tests.statements:
            points = statement.points
            if not points:
                count += 1
                left = self.evaluate_expression(statement.left_expression[0])
                if statement.right_expression:
                    right = self.evaluate_expression(statement.right_expression[0])
                    self.do_test('EQ', left, right, None);
                    yield '%s:%s:%s' % (self.doc.meta.data['Title'], '', count), self.do_test('EQ', left, right, count)
                continue

            blocks = self.select_blocks(points)
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

    def evaluate_expression(self, expression, block=None):
        context = Context(document=self.doc, block=block, value=None)
        
        def m1(item):
            if type(item).__name__ == 'Expression':
                return self.evaluate_expression(item, block)
            else:
                return item

        for transform in expression.transforms:
            if (context.error and transform.name != 'Catch'):
                continue
            function = self.Bridge._get_transform_function(transform.name)
            args = map(m1, transform.args)
            try:
                context.value = function(context, args)
            except Exception, e:
                context.error = e
        if context.error:
            raise context.error
        return context

    def parse(self):
        """parse the document"""
        parser = Parser(receiver=Builder(), start_token='document')
        parser.receiver.grammar = parser.grammar
        if (self.document):
            parser.open(self.document)
        elif (self.stream):
            parser.stream = self.stream
        else:
            raise Exception("Tried to run test without document or stream")
        parser.parse()
        self.parse_data(parser)
        return parser.receiver.document

    def parse_data(self, parser):
        builder = parser.receiver
        document = builder.document
        grammar = parser.grammar
        for file in document.meta.data['Data']:
            parser = Parser(
                receiver=Builder(),
                start_token='data'
            )
            parser.grammar = grammar
            if file == '_':
                parser.stream = builder.inline_data
            else:
                parser.open(os.path.join(self.base, file))
            parser.parse()
            document.data.blocks.extend(parser.receiver.blocks)

    def title(self):
        raise RunnerException("Don't use %s directly. Use a subclass" % self.__class__)

    def do_test(self, operator, left, right, lable=None):
        raise RunnerException("Don't use %s directly. Use a subclass" % self.__class__)
