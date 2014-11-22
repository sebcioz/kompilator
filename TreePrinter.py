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
        print "DECL"
        self.declarations.printTree(level)
        self.funDefs.printTree(level)

    @addToClass(AST.Declarations)
    def printTree(self, level):
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

    @addToClass(AST.FunDefs)
    def printTree(self, level):
        for funDef in self.funDefs:
            funDef.printTree(level)

    @addToClass(AST.FunDef)
    def printTree(self, level):
        indent(level, "FUNDEF")
        indent(level + 1, self.id.value)
        indent(level + 1, "RET " + self.type.value)

    @staticmethod
    def printAST(parsed):
        parsed.printTree(0)
