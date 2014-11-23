import AST
from utils import indent

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
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

    @addToClass(AST.Declarations)
    def printTree(self, level):
        indent(level, "DECL")
        for declaration in self.typedDeclarations:
            declaration.printTree(level+1)

    @addToClass(AST.TypedDeclarations)
    def printTree(self, level):
        indent(level, self.type)
        for declaration in self.declarations:
            declaration.printTree(level+1)

    @addToClass(AST.Declaration)
    def printTree(self, level):
        indent(level, "=")
        indent(level+1, self.id)
        indent(level+1, self.value)

    @addToClass(AST.FunDef)
    def printTree(self, level):
        indent(level, "FUNDEF")
        indent(level + 1, self.id.value)
        indent(level + 1, "RET " + self.type.value)

        for arg in self.args:
            arg.printTree(level + 1)

        self.compoundInstructions.printTree(level)

    @addToClass(AST.Arg)
    def printTree(self, level):
        indent(level, "ARG " + self.type.value + " " + self.id.value)

    @addToClass(AST.CompoundInstructions)
    def printTree(self, level):
        self.declarations.printTree(level+1)
        self.instructions.printTree(level)

    @addToClass(AST.PrintInstruction)
    def printTree(self, level):
        indent(level, "PRINT")
        self.expression.printTree(level+1)

    @addToClass(AST.Instructions)
    def printTree(self, level):
        for instruction in self.instructions:
            instruction.printTree(level+1)



    @addToClass(AST.Const)
    def printTree(self, level):
        indent(level, self.value)



    @staticmethod
    def printAST(parsed):
        parsed.printTree(0)
