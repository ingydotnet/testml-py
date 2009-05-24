
#from testml.document import Document
#from testml.parser import Parser

class RunnerException(Exception):
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
        # establish self.base the location of the data files
        self.setup()
        self.title()
        self.plan_begin()

        for statement in self.doc.tests.statements:
            blocks = self.select_blocks(statement.points)
            for block in blocks:
                left = self.evaluate_expression(
                        statement.primary_expression[0],
                        block,
                        )
                if statement.assertion_expression:
                    right = self.evaluation_express(
                            statement.assertion_expression[0],
                            block,
                            )
                    self.do_test('EQ', left, right, block.label)

        self.plan_end()

    def do_test(self, operator, left, right, lable=None):
        pass

    def parse(self):
        """parse the document"""
        pass
        #parser = Parser(self.document)
        #return parser.parse()
        
    def title(self):
        raise RunnerException("Don't use %s directly. Use a subclass" % self.__class__)

    def setup(self):
        raise RunnerException("Don't use %s directly. Use a subclass" % self.__class__)







