"""\
testml.runtime -
"""

# __ALL__ = ['Function']

class Function():
    def __init__(self, outer=None):
        self.type = 'Func'       # Functions are TestML typed objects
        self.outer = outer       # Parent/container function
        self.signature = []      # Input variable names
        self.namespace = {}      # Lexical scoped variable stash
        self.statements = []     # Exexcutable code statements
        self.data = []           # Data section scoped to this function

        # Runtime pointers to current objects.
        self.expression = None
        self.block = None

    def getvar(self, name):
        while self:
            if name in self.namespace:
                return self.namespace[name]
            self = self.outer
        return

    def setvar(self, name, object):
        self.namespace[name] = object
        return

    def forgetvar(self, name):
        del self.namespace[name]
        return

#-----------------------------------------------------------------------------
class Statement():
    def __init__(self):
        self.expression = Expression()
        self.assertion = None
        self.points = []

#-----------------------------------------------------------------------------
class Expression():
    def __init__(self):
        self.units = [];
        self.error = None

#-----------------------------------------------------------------------------
class Assertion():
    def __init__(self):
        self.expression = Expression()
# has 'name';

#-----------------------------------------------------------------------------
class Transform():
    def __init__(self, name=None, args=None):
        self.name = name
        if args is None:
            self.args = []
        else:
            self.args = args
        self.explicit_call = False

#-----------------------------------------------------------------------------
class Block():
    def __init__(self, label=''):
        self.label = label
        self.points = {}

#-----------------------------------------------------------------------------
class Object():
    def __init__(self, value=None):
        self.value = value

    def type_(self):
        type_ = self.__name__
        return type

    def runtime(self):
        return testml.runtime.self

    def str(self):
        t = self.type()
        raise Exception("Cast from %s to Str is not supported" % t)

    def num(self):
        t = self.type()
        raise Exception("Cast from %s to Num is not supported" % t)

    def bool(self):
        t = self.type()
        raise Exception("Cast from %s to Bool is not supported" % t)

    def list(self):
        t = self.type()
        raise Exception("Cast from %s to List is not supported" % t)

    def none(self):
        return testml.constant.None

#-----------------------------------------------------------------------------
class Str(Object):
    def __init__(self, value=None):
        Object.__init__(self, value=value)

# sub str { shift }
# sub num { TestML::Num->new(
#     value => ($_[0]->value =~ /^-?\d+(?:\.\d+)$/ ? ($_[0]->value + 0) : 0),
# )}
# sub bool {
#     length($_[0]->value) ? $TestML::Constant::True : $TestML::Constant::False
# }
# sub list { TestML::List->new(value => [split //, $_[0]->value]) }

#-----------------------------------------------------------------------------
class Num(Object):
    def __init__(self, value=None):
        Object.__init__(self, value=value)

# sub str { TestML::Str->new(value => $_[0]->value . "") }
# sub num { shift }
# sub bool { ($_[0]->value != 0) ? $TestML::Constant::True : $TestML::Constant::False }
# sub list {
#     my $list = [];
#     $#{$list} = int($_[0]) -1;
#     TestML::List->new(value =>$list);
# }
# 
# #-----------------------------------------------------------------------------
# package TestML::Bool;
# use TestML::Object -base;
# 
# sub str { TestML::Str->new(value => $_[0]->value ? "1" : "") }
# sub num { TestML::Num->new(value => $_[0]->value ? 1 : 0) }
# sub bool { shift }
# 
# #-----------------------------------------------------------------------------
# package TestML::List;
# use TestML::Object -base;
# sub list { shift }
# 
# #-----------------------------------------------------------------------------
# package TestML::None;
# use TestML::Object -base;
# 
# sub str { Str('') }
# sub num { Num(0) }
# sub bool { $TestML::Constant::False }
# sub list { List([]) }
# 
# #-----------------------------------------------------------------------------
# package TestML::Error;
# use TestML::Object -base;
# 
# #-----------------------------------------------------------------------------
# package TestML::Native;
# use TestML::Object -base;
# 
# package TestML::Constant;
# 
# our $True = TestML::Bool->new(value => 1);
# our $False = TestML::Bool->new(value => 0);
# our $None = TestML::None->new;
# 
