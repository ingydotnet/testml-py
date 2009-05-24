
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
                'TestMLBlockMarker': '===',
                'TestMLPointMarker': '---',
                }


class Tests(object):
    def __init__(self):
        self.statements = []


class Statement(object):
    def __init__(self):
        self.points = []
        self.primary_expression = []
        self.assertion_operator = None
        self.assertion_expression = []

class Exression(object):
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
        self.insert_expression_here = []
        self.current_expression = []
        self.blocks = []
        self.arguments = []

        self.current_statement = None
        self.inline_data = None
        self.current_block = None
        self.point_name = None
        self.transform_name = None

    def got_document(self):
        data_files = self.document.meta.data['Data']
        if not data_files:
            data_file.append('_')
        
    def got_meta_testml_statement(self, version):
        self.document.meta.data['TestML'] = version

    def got_meta_statement(self, key, value):
        try:
            self.document.meta.data['key'].append(value)
        except AttributeError:
            self.document.meta.data['key'] = value

    def try_test_statement(self):
        self.current_statement(Statement())
        self.insert_expression_here.append(self.current_statement.primary_expression)

    def got_test_statement(self):
        statement = self.current_statement
        statement.points = sorted(list.set(statment.points))
        self.document.tests.statements.append(statement)
        self.current_statement = None

    def not_test_statement(self):
        self.current_statement = None

    def try_test_expression(self):
        self.current_expression.append(Exression())

    def got_test_expression(self):
        self.insert_expression_here[-1].append(self.current_expression.pop())

    def not_test_expression(self):
        self.current_expression.pop()

    def got_data_point(self, name):
        self.current_statement.points.append(name)
        self.current_expression[-1].transforms.append(Transform(name='Point', args=name))

    def try_transform_call(self):
        self.arguments = []

    def got_single_quoted_string(self, value):
        self.arguments.append(value)

    def got_transform_name(self, name):
        self.transform_name = name

    def got_transform_class(self):
        name = self.transform_name
        self.current_expression[-1].transforms.append(Transform(name=name, args=self.arguments))

    def got_assertion_operator(self):
        self.insert_expression_here.append(self.current_statement.assertion_expression)

    def got_data_section(self, data):
        self.inline_data = data

    def try_data_block(self):
        self.current_block = Block()

    def got_data_block(self):
        self.blocks.append(self.current_block)

    def got_block_label(self, label):
        self.current_block.label = lable

    def got_user_point_name(self, name):
        self.point_name = name

    def got_point_lines(self, lines):
        self.current_block.points[self.point_name] = lines

    def got_point_phrase(self, phrase):
        self.current_block.points[self.point_name] = phrase

