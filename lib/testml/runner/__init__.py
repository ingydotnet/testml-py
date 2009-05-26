
from testml.document import Document, Builder
from testml.parser import Parser

import os

class RunnerException(Exception):
    pass

class Topic(object):
    def __init__(self, document=None, block=None, value=None):
        self.document = document
        self.block = block
        self.value = value

# field 'document'
# field 'block'
# field 'value'
    pass

class Runner(object):

    def __init__(self, document=None, bridge=None):
        self.document = document
        self.bridge = bridge
        self.doc = self.parse()
        self.Bridge = self.init_bridge()

    def init_bridge(self):
        """Initialize the Bridge Class. Will throw if it can't import."""
        return self.bridge()


    def run(self):
        # TODO establish self.base the location of the data files
        self.setup()
        self.title()
        self.plan_begin()

        for statement in self.doc.tests.statements:
            blocks = self.select_blocks(statement.points)

            for block in blocks:
                left = self.evaluate_expression(statement.primary_expression[0], block)
                if statement.assertion_expression:
                    right = self.evaluation_express(statement.assertion_expression[0], block)
                    yield self.do_test('EQ', left, right, block.label)

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
        topic = Topic(document=self.doc, block=block, value=None)
        
        for transform in expression.transforms:
            function = self.Bridge.get_transform_function(transform.name)
            topic.value = function(topic, transform.args)
        return topic

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
                parser.open(os.path.join(self.bag, file))
            parser.parse()
            document.data.blocks.extend(parser.receiver.blocks)

    def title(self):
        raise RunnerException("Don't use %s directly. Use a subclass" % self.__class__)

    def setup(self):
        raise RunnerException("Don't use %s directly. Use a subclass" % self.__class__)

    def do_test(self, operator, left, right, lable=None):
        raise RunnerException("Don't use %s directly. Use a subclass" % self.__class__)
