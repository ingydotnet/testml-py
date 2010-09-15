"""\
testml.compiler - compile testml documents
"""

import sys
import re
import testml.grammar
from testml.runtime import *

# from testml.XXX import *

class Compiler():
    def __init__(self, debug=False):
        self.base = None
        self.debug = debug

    def compile(self, file_):
        if type(file_) == str and "\n" not in file_:
            m = re.match(r'(.*)/(.*)', file_)
            if not match:
                raise Exception("Invalid file name")
            file_ = m.groups()[1]
            self.base = m.groups()[0]
        input = (
            file_ if (type(file_) == str and "\n" in file_)
            else file(file_).read()
        )
        result = self.preprocess(input, 'top')
        code = result['code']
        data = result['data']
        debug = self.debug
        if 'DebugPegex' in result:
            debug = result['DebugPegex']
        grammar = testml.grammar.Grammar(
            receiver=Receiver(),
            debug=debug,
        )
        if not grammar.parse(code, 'code_section'):
            raise Exception("Parse TestML code section failed")
        self.fixup_grammar(grammar, result)
        if not grammar.parse(data, 'data_section'):
            raise Exception("Parse TestML data section failed")
        if result.get('DumpAST', False):
            XXX(grammar.receiver.function)
        return grammar.receiver.function

    def preprocess(self, text, top):
        parts = re.compile(r'^((?:\%\w+.*|\#.*|\ *)\n)', re.M).split(text)
        text = ''
        result = {
            'TestML': '',
            'DataMarker': '',
            'BlockMarker': '===',
            'PointMarker': '---',
        }
        order_error = False
        for part in parts:
            if not len(part):
                continue
            if re.match(r'^(\#.*|\ *)\n', part):
                text += "\n"
                continue
            m = re.match('^%(\w+)\s*(.*?)\s*\n', part)
            if m:
                (directive, value) = m.groups()
                text += "\n"
                if directive == 'TestML':
                    if not re.match(r'^\d+\.\d+$', value):
                        raise Exception("Invalid TestML directive")
                    if result['TestML']:
                        raise Exception("More than one TestML directive found")
                    result['TestML'] = value
                    continue
                if not result['TestML']:
                    order_error = True
                if directive == 'Include':
                    text += self.preprocess(self.slurp(value))['text']
                elif directive in ['DataMarker', 'BlockMarker', 'PointMarker']:
                    result['directive'] = value
                elif directive in ['DebugPegex', 'DumpAST']:
                    if not len(value):
                        value = True
                    result['directive'] = value
                else:
                    raise Exception("Unknown TestML directive 'directive'")
            else:
                if text and not result['TestML']:
                    order_error = True
                text += part
        if top:
            if not result['TestML']:
                raise Exception("No TestML directive found")
            if order_error:
                raise Exception(
                    "%TestML directive must be the first (non-comment) statement"
                )
            if not result['DataMarker']:
                result['DataMarker'] = result['BlockMarker']
            DataMarker = result['DataMarker']
            split = text.find("\n%s" % DataMarker)
            if split >= 0:
                result['code'] = text[0:split + 1]
                result['data'] = text[split + 1:]
            else:
                result['code'] = text
                result['data'] = ''
            result['code'] = (
                re.sub(r'^\\(\\*[\%\#])', r'\1', result['code'], re.M)
            )
            result['data'] = (
                re.sub(r'^\\(\\*[\%\#])', r'\1', result['data'], re.M)
            )
        else:
            result['text'] = text
        return result

    def fixup_grammar(self, grammar, hash):
        namespace = grammar.receiver.function.namespace
        namespace['TestML'] = hash['TestML']

        grammar = grammar.grammar
        point_lines = grammar['point_lines']['+re']

        block_marker = hash['BlockMarker']
        if block_marker:
            block_marker = re.sub(r'([\$\%\^\*\+\?\|])', r'\1', block_marker)
            grammar['block_marker']['+re'] = block_marker
            point_lines = re.sub('===', block_marker, point_lines)

        point_marker = hash['PointMarker']
        if point_marker:
            point_marker = re.sub(r'([\$\%\^\*\+\?\|])', r'\1', point_marker)
            grammar['point_marker']['+re'] = point_marker
            point_lines = re.sub('===', point_marker, point_lines)

        grammar['point_lines']['+re'] = point_lines


# sub slurp {
#     my $self = shift;
#     my $file = shift;
#     my $fh;
#     if (ref($file)) {
#         $fh = $file;
#     }
#     else {
#         my $path = join '/', $self->base, $file;
#         open $fh, $path
#             or die "Can't open '$path' for input: $!";
#     }
#     local $/;
#     return <$fh>;
# }


#-----------------------------------------------------------------------------
class Receiver():

    ESCAPES = {
        '\\': '\\',
        "'": "'",
        'n': "\n",
        't': "\t",
        '0': "\0",
    }

    def __init__(self):
        self.function = Function()

        self.stack = []
        self.block = None
        self.string = None
        self.point_name = None


    def got_single_quoted_string(self, groups):
        string = groups[0]
        def f(m):
            return ESCAPES.get(m.groups()[0])
        string = re.sub(r"\\([\\\'])", f, string)
        self.string = string

    def got_double_quoted_string(self, groups):
        string = groups[0]
        def f(m):
            return ESCAPES.get(m.groups()[0])
        string = re.sub(r"\\([\\\'])", f, string)
        self.string = string

    def got_unquoted_string(self, groups):
        self.string = groups[0]

    def try_assignment_statement(self, xxx):
        self.function.statements.append(Statement())
        expression = self.function.statements[-1].expression
        if not expression.units:
            expression.units.append(None)
        expression.units[0] = Transform(name='Set')
        self.function.statements[-1].expression = expression
        self.stack.append(Expression())

    def got_assignment_statement(self, x):
        units = self.function.statements[-1].expression.units
        units[0].args.append(self.stack.pop())

    def not_assignment_statement(self, xxx):
        self.function.statements.pop()
        self.stack.pop()

    def got_variable_name(self, groups):
        variable_name = groups[0]
        args = self.function.statements[-1].expression.units[0].args
        if not args:
            args.append(None)
        args[0] = variable_name

    def try_code_statement(self, xxx):
        self.function.statements.append(Statement())
        self.stack.append(self.function.statements[-1].expression)

    def got_code_statement(self, xxx):
        self.stack.pop()

    def not_code_statement(self, xxx):
        self.function.statements.pop()
        self.stack.pop()

    def got_point_object(self, groups):
        point_name = groups[0][1:]
        self.stack[-1].units.append(
            Transform(name='Point', args=[point_name])
        )
        self.function.statements[-1].points.append(point_name)

    def try_function_object(self, xxx):
        function = Function(outer=self.function)
        self.function =function

    def got_function_object(self, xxx):
        self.stack[-1].units.append(self.function)
        self.function = self.function.outer

    def not_function_object(self, xxx):
        self.function = self.function.outer

    def got_function_variable(self, groups):
        self.function.signature.append(groups[0])

    def try_transform_object(self, xxx):
        self.stack[-1].units.append(Transform())

    def not_transform_object(self, xxx):
        self.stack[-1].units.pop()

    def got_transform_name(self, groups):
        self.stack[-1].units[-1].name = groups[0]

    def got_transform_argument_list(self, xxx):
        self.stack[-1].units[-1].explicit_call = True

    def try_transform_argument(self, xxx):
        self.stack.append(Expression())

    def got_transform_argument(self, xxx):
        argument = self.stack.pop()
        self.stack[-1].units[-1].args.append(argument)

    def not_transform_argument(self, xxx):
        self.stack.pop()

    def got_string_object(self, xxx):
        self.stack[-1].units.append(Str(value=self.string))

    def got_number_object(self, groups):
        self.stack[-1].units.append(Num(value=groups[0]))

    def try_assertion_call(self, xxx):
        self.function.statements[-1].assertion = Assertion()
        self.stack.append(
            self.function.statements[-1].assertion.expression
        )

    def got_assertion_call(self, xxx):
        self.stack.pop()

    def not_assertion_call(self, xxx):
        self.function.statements[-1].assertion = None
        self.stack.pop()

    def got_assertion_eq(self, xxx):
        self.function.statements[-1].assertion.name = 'EQ'

    def got_assertion_ok(self, xxx):
        self.function.statements[-1].assertion.name = 'OK'

    def got_assertion_has(self, xxx):
        self.function.statements[-1].assertion.name('HAS')

    def got_block_label(self, groups):
        self.block = Block(label=groups[0])

    def got_point_name(self, groups):
        self.point_name = groups[0]

    def got_point_phrase(self, groups):
        self.block.points[self.point_name] = groups[0]

    def got_point_lines(self, groups):
        self.block.points[self.point_name] = groups[0]

    def got_data_block(self, xxx):
        self.function.data.append(self.block)
