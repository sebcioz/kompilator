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
    def __init__(self, declarations, funDefs, instructions):
        self.declarations = declarations
        self.funDefs = funDefs
        self.instructions = instructions

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

class WhileInstruction(Instruction):
    def __init__(self, condition, instruction):
        super(WhileInstruction, self).__init__()
        self.condition = condition
        self.instruction = instruction

class LabeledInstruction(Instruction):
    def __init__(self, id, instruction):
        super(LabeledInstruction, self).__init__()
        self.id = id
        self.instruction = instruction

class AssignmentInstruction(Instruction):
    def __init__(self, id, expression):
        super(AssignmentInstruction, self).__init__()
        self.id = id
        self.expression = expression

class ChoiceInstruction(Instruction):
    def __init__(self, condition, instruction):
        super(ChoiceInstruction, self).__init__()
        self.condition = condition
        self.instruction = instruction


class ChoiceElseInstruction(Instruction):
    def __init__(self, condition, instruction, elseInstruction):
        super(ChoiceElseInstruction, self).__init__()
        self.condition = condition
        self.instruction = instruction
        self.elseInstruction = elseInstruction

class RepeatInstruction(Instruction):
    def __init__(self, instructions, condition):
        super(RepeatInstruction, self).__init__()
        self.instructions = instructions
        self.condition = condition

class Operator(Node):
    def __init__(self, leftOperand, rightOperand):
        super(Operator, self).__init__()
        self.leftOperand = leftOperand
        self.rightOperand = rightOperand
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

class FunctionCallOperator(Node):
    def __init__(self, id, arguments):
        self.id = id
        self.arguments = arguments


class ReturnInstruction(Instruction):
    def __init__(self, expression):
        super(ReturnInstruction, self).__init__()
        self.expression = expression

class ContinueInstruction(Instruction):
    pass

class BreakInstruction(Instruction):
    pass