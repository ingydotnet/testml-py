import sys; sys.path.insert(0, '.')
from package.unittest import *

# from testml.XXX import *

class TestCompile(TestCase):
    def test_compile(self):
        from testml.compiler import Compiler

        testml = """
# A comment
%TestML 1.0

Plan = 2;
Title = "O HAI TEST";

*input.uppercase() == *output;

=== Test mixed case string
--- input: I Like Pie
--- output: I LIKE PIE

=== Test lower case string
--- input: i love lucy
--- output: I LOVE LUCY
"""

        func = Compiler().compile(testml)
        self.assertTrue(func, 'TestML string matches against TestML grammar')
        self.assertEquals(func.namespace['TestML'], '1.0', 'Version parses')
        self.assertEquals(func.statements[0].expression.units[0].args[1].units[0].value, '2', 'Plan parses')
        self.assertEquals(func.statements[1].expression.units[0].args[1].units[0].value, 'O HAI TEST', 'Title parses')
        self.assertEquals(len(func.statements), 3, 'Three test statements')
        statement = func.statements[2]
        self.assertEquals('-'.join(statement.points), 'input-output', 'Point list is correct')
        self.assertEquals(len(statement.expression.units), 2, 'Expression has two units')
        expression = statement.expression
        self.assertEquals(expression.units[0].name, 'Point', 'First sub is a Point')
        self.assertEquals(expression.units[0].args[0], 'input', 'Point name is "input"')
        self.assertEquals(expression.units[1].name, 'uppercase', 'Second sub is "uppercase"')
        self.assertEquals(statement.assertion.name, 'EQ', 'Assertion is "EQ"')
        expression = statement.assertion.expression
        self.assertEquals(len(expression.units), 1, 'Right side has one part')
        self.assertEquals(expression.units[0].name, 'Point', 'First sub is a Point')
        self.assertEquals(expression.units[0].args[0], 'output', 'Point name is "output"')
        self.assertEquals(len(func.data), 2, 'Two data blocks')
        (block1, block2) = func.data
        self.assertEquals(block1.label, 'Test mixed case string', 'Block 1 label ok')
        self.assertEquals(block1.points['input'], 'I Like Pie', 'Block 1, input point')
        self.assertEquals(block1.points['output'], 'I LIKE PIE', 'Block 1, output point')
        self.assertEquals(block2.label, 'Test lower case string', 'Block 2 label ok')
        self.assertEquals(block2.points['input'], 'i love lucy', 'Block 2, input point')
        self.assertEquals(block2.points['output'], 'I LOVE LUCY', 'Block 2, output point')

if __name__ == '__main__':
    main()
