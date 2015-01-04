import AST
from utils import indent


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.Program)
    def printTree(self, level):
        self.declarations.printTree(level)

        for funDef in self.funDefs:
            funDef.printTree(level)

        self.instructions.printTree(level)


    @addToClass(AST.Declarations)
    def printTree(self, level):
        indent(level, "DECL")
        for declaration in self.typedDeclarations:
            declaration.printTree(level + 1)

    @addToClass(AST.TypedDeclarations)
    def printTree(self, level):
        indent(level, self.type)
        for declaration in self.declarations:
            declaration.printTree(level + 1)

    @addToClass(AST.Declaration)
    def printTree(self, level):
        indent(level, "=")
        indent(level + 1, self.id)
        indent(level + 1, self.value)

    @addToClass(AST.FunDef)
    def printTree(self, level):
        indent(level, "FUNDEF")
        indent(level + 1, self.id.value)
        indent(level + 1, "RET " + self.type.value)

        for arg in self.args:
            arg.printTree(level + 1)

        self.compoundInstructions.printTree(level + 1)

    @addToClass(AST.Arg)
    def printTree(self, level):
        indent(level, "ARG " + self.type.value + " " + self.id.value)

    @addToClass(AST.CompoundInstructions)
    def printTree(self, level):
        self.declarations.printTree(level)
        self.instructions.printTree(level)

    @addToClass(AST.PrintInstruction)
    def printTree(self, level):
        indent(level, "PRINT")
        self.expression.printTree(level + 1)

    @addToClass(AST.Instructions)
    def printTree(self, level):
        for instruction in self.instructions:
            instruction.printTree(level)

    @addToClass(AST.WhileInstruction)
    def printTree(self, level):
        indent(level, "WHILE")
        self.condition.printTree(level + 1)
        self.instruction.printTree(level + 1)

    @addToClass(AST.LabeledInstruction)
    def printTree(self, level):
        indent(level, "LABELED")
        self.id.printTree(level + 1)
        self.instruction.printTree(level + 1)

    @addToClass(AST.AssignmentInstruction)
    def printTree(self, level):
        indent(level, "=")
        self.id.printTree(level + 1)
        self.expression.printTree(level + 1)


    @addToClass(AST.ChoiceInstruction)
    def printTree(self, level):
        indent(level, "IF")
        self.condition.printTree(level + 1)
        self.instruction.printTree(level + 1)

    @addToClass(AST.ChoiceElseInstruction)
    def printTree(self, level):
        indent(level, "IF")
        self.condition.printTree(level + 1)
        self.instruction.printTree(level + 1)
        indent(level, "ELSE")
        self.elseInstruction.printTree(level + 1)

    @addToClass(AST.RepeatInstruction)
    def printTree(self, level):
        indent(level, "REPEAT")
        self.instructions.printTree(level + 1)
        indent(level, "UNTIL")
        self.condition.printTree(level + 1)

    @addToClass(AST.Operator)
    def printTree(self, level):
        indent(level, self.sign())
        self.leftOperand.printTree(level + 1)
        self.rightOperand.printTree(level + 1)

    @addToClass(AST.GroupingOperator)
    def printTree(self, level):
        self.operand.printTree(level)

    @addToClass(AST.FunctionCallOperator)
    def printTree(self, level):
        indent(level, "CALL")
        self.id.printTree(level + 1)
        for argument in self.arguments:
            argument.printTree(level + 1)

    @addToClass(AST.ReturnInstruction)
    def printTree(self, level):
        indent(level, "RETURN")
        self.expression.printTree(level + 1)

    @addToClass(AST.ContinueInstruction)
    def printTree(self, level):
        indent(level, "CONTINUE")

    @addToClass(AST.BreakInstruction)
    def printTree(self, level):
        indent(level, "BREAK")

    @staticmethod
    def printAST(parsed):
        parsed.printTree(0)

    @addToClass(AST.Const)
    def printTree(self, level):
        indent(level, self.value)


