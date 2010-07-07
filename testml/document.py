import re

class Document(object):
    def __init__(self):
        self.meta = Meta()
        self.tests = Tests()
        self.data = Data()


class Meta(object):
    def __init__(self):
        self.data = {
            'TestML': '',
            'Data': [],
            'Title': '',
            'Plan': 0,
            'BlockMarker': '===',
            'PointMarker': '---',
        }


class Tests(object):
    def __init__(self):
        self.statements = []


class Statement(object):
    def __init__(self):
        self.points = []
        self.left_expression = []
        self.assertion_operator = None
        self.right_expression = []

class Expression(object):
    def __init__(self):
        self.transforms = []


class Transform(object):
    def __init__(self, name=None, args=None):
        if not args:
            args = []
        self.name = name
        self.args = args


class Data(object):
    def __init__(self):
        self.blocks = []


class Block(object):
    def __init__(self):
        self.label = ''
        self.points = {}


class Builder(object):

    def __init__(self):
        self.document = Document()
        self.grammar = None

        self.current_statement = None
        self.insert_expression_here = None
        self.current_expression = []
        self.inline_data = None

        self.current_block = None
        self.blocks = []
        self.point_name = None
        self.transform_name = None
        self.arguments = []

    def got_document(self, arguments):
        data_files = self.document.meta.data['Data']
        if not data_files:
            data_files.append('_')
        
    def got_meta_testml_statement(self, arguments):
        version = arguments[0]
        self.document.meta.data['TestML'] = version

    def got_meta_statement(self, arguments):
        key, value = arguments[0:2]
        try:
            self.document.meta.data[key].append(value)
        except AttributeError:
            self.document.meta.data[key] = value
        if (key == 'BlockMarker' or key == 'PointMarker'):
            def r1(m):
                if m.group(1):
                    return m.group(1) + '_' + m.group(2).lower()
                else:
                    return m.group(2).lower()

            key = re.sub(r'([a-z])?([A-Z])', r1, key)
            value = re.sub(r'([\$\%\^\*\+\?\|])', lambda m: '\\' + m.group(1), value)
            self.grammar[key] = '/' + value + '/'

    def try_test_statement(self, arguments):
        self.current_statement = Statement()
        self.insert_expression_here = self.current_statement.left_expression

    def got_test_statement(self, arguments):
        statement = self.current_statement
        statement.points = sorted(list(set(statement.points)))
        self.document.tests.statements.append(statement)
        self.current_statement = None

    def not_test_statement(self, arguments):
        self.current_statement = None

    def try_argument(self, arguments):
        self.current_expression.append(Expression())

    def got_argument(self, arguments):
        self.arguments.append(self.current_expression.pop())

    def not_argument(self, arguments):
        self.current_expression.pop()

    def try_test_expression(self, arguments):
        self.current_expression.append(Expression())

    def got_test_expression(self, arguments):
        self.insert_expression_here.append(self.current_expression.pop())

    def not_test_expression(self, arguments):
        self.current_expression.pop()

    def got_data_point(self, arguments):
        name = arguments[0]
        assert(name[0] == '*')
        name = name.lstrip('*')
        self.current_statement.points.append(name)
        self.current_expression[-1].transforms.append(
            Transform(name='Point', args=[name])
        )

    def try_transform_call(self, arguments):
        self.arguments = []

    def got_single_quoted_string(self, arguments):
        # TODO apply escapes
        self.current_expression[-1].transforms.append(
            Transform(name='String', args=arguments)
        )

    def got_double_quoted_string(self, arguments):
        # TODO apply escapes
        self.current_expression[-1].transforms.append(
            Transform(name='String', args=arguments)
        )

    def got_transform_name(self, arguments):
        self.transform_name = arguments[0]

    def got_transform_call(self, arguments):
        name = self.transform_name
        self.current_expression[-1].transforms.append(Transform(name=name, args=self.arguments))
        self.arguments = []

    def got_assertion_operator(self, arguments):
        self.insert_expression_here = self.current_statement.right_expression

    def got_data_section(self, arguments):
        self.inline_data = arguments[0]

    def try_data_block(self, arguments):
        self.current_block = Block()

    def got_data_block(self, arguments):
        self.blocks.append(self.current_block)

    def got_block_label(self, arguments):
        self.current_block.label = arguments[0]

    def got_user_point_name(self, arguments):
        self.point_name = arguments[0]

    def got_point_lines(self, arguments):
        self.current_block.points[self.point_name] = arguments[0]

    def got_point_phrase(self, arguments):
        self.current_block.points[self.point_name] = arguments[0]
