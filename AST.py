import utils

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
    def __init__(self, declarations, funDefs):
        self.declarations = declarations
        self.funDefs = funDefs

class Declarations(Node):
    def __init__(self, typedDeclarations):
        self.typedDeclarations = typedDeclarations

    @staticmethod
    def mapTypedDeclarations(typedDeclarations):
        declarations = utils.flatten(typedDeclarations)
        grouped = {}

        for declaration in declarations:
            if not grouped.has_key(declaration.type.value):
                grouped[declaration.type.value] = TypedDeclarations(declaration.type, [])
            grouped[declaration.type.value].declarations.extend(declaration.declarations)


        return Declarations(grouped.values())

class TypedDeclarations(Node):
    def __init__(self, type, declarations):
        self.type = type
        self.declarations = declarations

class Declaration(Node):
    def __init__(self, id, value):
        self.id = id
        self.value = value

class FunDef(Node):
    def __init__(self, type, id, args, compoundInstructions):
        self.type = type
        self.id = id
        self.args = args
        self.compoundInstructions = compoundInstructions

class Arg(Node):
    def __init__(self, type, id):
        self.type = type
        self.id = id

class String(Const):
    pass

class Type(Const):
    pass

class ID(Const):
    pass


class CompoundInstructions(Node):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions

class Instructions(Node):
    def __init__(self, instructions):
        self.instructions = instructions

class Instruction(Node):
    pass

class PrintInstruction(Instruction):
    def __init__(self, expression):
        super(PrintInstruction, self).__init__()
        self.expression = expression