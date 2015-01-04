import utils
from scope import SymbolScope


class Node(object):
    def __init__(self):
        self.scope = None
        self.children = []
        self.parent = None
        self.line = None
        self.column = None

    def set_parents(self):
        for child in self.children:
            child.parent = self
            child.set_parents()

    def set_scope(self, scope):
        self.scope = scope
        for child in self.children:
            child.set_scope(scope)

    def accept(self, visitor):
        return visitor.visit(self)

    def set_position(self, line, column):
        self.line = line
        self.column = column


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
    def __init__(self, declarations, funDefs, instructions):
        super(Program, self).__init__()
        self.declarations = declarations
        self.funDefs = funDefs
        self.instructions = instructions

        self.children = [declarations] + funDefs + [instructions]

    def set_scope(self, scope=None):
        self.scope = SymbolScope()
        self.scope.parent = scope
        for child in self.children:
            child.set_scope(self.scope)


class Declarations(Node):
    def __init__(self, typedDeclarations):
        super(Declarations, self).__init__()
        self.typedDeclarations = typedDeclarations
        self.children = typedDeclarations

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
        super(TypedDeclarations, self).__init__()
        self.type = type
        self.declarations = declarations
        self.children = declarations
        for declaration in self.declarations:
            declaration.id.type = self.type


class Declaration(Node):
    def __init__(self, id, value):
        super(Declaration, self).__init__()
        self.id = id
        self.value = value

        self.children = [id, value]


class FunDef(Node):
    def __init__(self, type, id, args, compoundInstructions):
        super(FunDef, self).__init__()
        self.type = type
        self.id = id
        self.id.type = type
        self.args = args
        self.compoundInstructions = compoundInstructions

        self.children = [compoundInstructions]

    def set_scope(self, scope):
        self.scope = SymbolScope()
        self.scope.parent = scope

        for child in self.children:
            child.set_scope(scope, preset_scope=self.scope)


class Arg(Node):
    def __init__(self, type, id):
        super(Arg, self).__init__()
        self.type = type
        self.id = id
        self.id.type = type


class String(Const):
    pass


class Type(Const):
    pass


class ID(Const):
    def __eq__(self, other):
        if type(other) is str:
            return False
        return self.value == other.value

    def __hash__(self):
        return self.value.__hash__()


class CompoundInstructions(Node):
    def __init__(self, declarations, instructions):
        super(CompoundInstructions, self).__init__()
        self.declarations = declarations
        self.instructions = instructions
        self.children = [declarations, instructions]

    def set_scope(self, scope, preset_scope=None):
        if preset_scope is None:
            self.scope = SymbolScope()
        else:
            self.scope = preset_scope

        self.scope.parent = scope
        for child in self.children:
            child.set_scope(self.scope)


class Instructions(Node):
    def __init__(self, instructions):
        super(Instructions, self).__init__()
        self.instructions = instructions
        self.children = instructions


class Instruction(Node):
    pass


class PrintInstruction(Instruction):
    def __init__(self, expression):
        super(PrintInstruction, self).__init__()
        self.expression = expression
        self.children = [expression]


class WhileInstruction(Instruction):
    def __init__(self, condition, instruction):
        super(WhileInstruction, self).__init__()
        self.condition = condition
        self.instruction = instruction
        self.children = [condition, instruction]


class LabeledInstruction(Instruction):
    def __init__(self, id, instruction):
        super(LabeledInstruction, self).__init__()
        self.id = id
        self.instruction = instruction
        self.children = [instruction]


class AssignmentInstruction(Instruction):
    def __init__(self, id, expression):
        super(AssignmentInstruction, self).__init__()
        self.id = id
        self.expression = expression

        self.children = [expression, id]


class ChoiceInstruction(Instruction):
    def __init__(self, condition, instruction):
        super(ChoiceInstruction, self).__init__()
        self.condition = condition
        self.instruction = instruction

        self.children = [condition, instruction]


class ChoiceElseInstruction(Instruction):
    def __init__(self, condition, instruction, elseInstruction):
        super(ChoiceElseInstruction, self).__init__()
        self.condition = condition
        self.instruction = instruction
        self.elseInstruction = elseInstruction

        self.children = [condition, instruction, elseInstruction]


class RepeatInstruction(Instruction):
    def __init__(self, instructions, condition):
        super(RepeatInstruction, self).__init__()
        self.instructions = instructions
        self.condition = condition

        self.children = [instructions] + [condition]


class Operator(Node):
    def __init__(self, leftOperand, rightOperand):
        super(Operator, self).__init__()
        self.leftOperand = leftOperand
        self.rightOperand = rightOperand

        self.children = [leftOperand, rightOperand]

    def sign(self):
        pass


class SumOperator(Operator):
    def sign(self):
        return "+"


class MultiplyOperator(Operator):
    def sign(self):
        return "*"


class DifferenceOperator(Operator):
    def sign(self):
        return "-"


class DivOperator(Operator):
    def sign(self):
        return "/"


class LogicalAndOperator(Operator):
    def sign(self):
        return "AND"


class EqualOperator(Operator):
    def sign(self):
        return "=="


class ModuloOperator(Operator):
    def sign(self):
        return "%"


class BitXorOperator(Operator):
    def sign(self):
        return "^"


class BitAndOperator(Operator):
    def sign(self):
        return "&"


class BitOrOperator(Operator):
    def sign(self):
        return "|"


class ShiftLeftOperator(Operator):
    def sign(self):
        return "<<"


class ShiftRightOperator(Operator):
    def sign(self):
        return ">>"


class LogicalOrOperator(Operator):
    def sign(self):
        return "||"


class NotEqualOperator(Operator):
    def sign(self):
        return "!="


class GreaterThanOperator(Operator):
    def sign(self):
        return ">"


class GreaterEqualOperator(Operator):
    def sign(self):
        return ">="


class LowerThanOperator(Operator):
    def sign(self):
        return "<"


class LowerEqualOperator(Operator):
    def sign(self):
        return "<="


class GroupingOperator(Node):
    def __init__(self, operand):
        super(GroupingOperator, self).__init__()
        self.operand = operand
        self.children = [operand]


class FunctionCallOperator(Node):
    def __init__(self, id, arguments):
        super(FunctionCallOperator, self).__init__()
        self.id = id
        self.arguments = arguments
        self.children = arguments + [id]


class ReturnInstruction(Instruction):
    def __init__(self, expression):
        super(ReturnInstruction, self).__init__()
        self.expression = expression
        self.children = [expression]


class ContinueInstruction(Instruction):
    pass


class BreakInstruction(Instruction):
    pass