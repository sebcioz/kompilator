class Node(object):
    pass
    #def __repr__(self):

        #raise Exception("__repr__ not defined in class " + self.__class__.__name__)


class Const(Node):
    def __init__(self, value):
        super(Const, self).__init__()
        self.value = value

    def __repr__(self):
        return str(self.value)


class Integer(Const):
    def __init__(self, value):
        super(Integer, self).__init__(int(value))


class Float(Const):

    def __init__(self, value):
        super(Float, self).__init__(float(value))

class Program(Node):
    def __init__(self, declarations):
        self.declarations = declarations

class Declarations(Node):
    def __init__(self, typedDeclarations):
        self.typedDeclarations = typedDeclarations

class TypedDeclarations(Node):
    def __init__(self, type, declarations):
        self.type = type
        self.declarations = declarations

class Declaration(Node):
    def __init__(self, id, value):
        self.id = id
        self.value = value


class String(Const):
    pass

class Type(Const):
    pass

class ID(Const):
    pass

