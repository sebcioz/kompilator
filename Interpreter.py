
import AST
from scope import ValueScope
from Memory import *
from Exceptions import  *
from visit import *

operation = {}

operation["+"] = lambda a,b: a + b
operation["-"] = lambda a,b: a - b
operation["*"] = lambda a,b: a * b
operation["/"] = lambda a,b: a / b
operation["%"] = lambda a,b: a % b

operation["|"] = lambda a,b: a | b
operation["&"] = lambda a,b: a & b
operation["^"] = lambda a,b: a ^ b
operation["||"] = lambda a,b: a or b
operation["&&"] = lambda a,b: a and b
operation[">>"] = lambda a,b: a >> b
operation["<<"] = lambda a,b: a << b

operation["=="] = lambda a,b: a == b
operation["!="] = lambda a,b: a != b
operation[">="] = lambda a,b: a >= b
operation["<="] = lambda a,b: a <= b
operation["<"] = lambda a,b: a < b
operation[">"] = lambda a,b: a > b
operation["="] = lambda a,b: a

# dict used by a workaround to no-return-error
default_value = {}
default_value["int"] = 0
default_value["float"] = 0.0
default_value["string"] = ""

class Interpreter(object):

    @on('node')
    def visit(self, node):
        pass




    @when(AST.Integer)
    def visit(self, node):
        return int(node.value)

    @when(AST.Float)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        # no eval certainly
        return str(node.value)[1:-1]
    #
    @when(AST.Program)
    def visit(self, node):
        self.globalScope = ValueScope()
        self.stack = MemoryStack( self.globalScope )
        self.curScope = self.globalScope

        node.declarations.accept(self)

        for funDef in node.funDefs:
            funDef.accept(self)

        node.instructions.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.Declarations)
    def visit(self, node):
        for typedDeclaration in node.typedDeclarations:
            typedDeclaration.accept(self)

    @when(AST.TypedDeclarations)
    def visit(self, node):
        for declaration in node.declarations:
            declaration.accept(self)


    @when(AST.ID)
    def visit(self, node):
        return self.curScope[ node ]

    @when(AST.Declaration)
    def visit(self, node):
         self.curScope[ node.id ] = node.value.accept(self)

    @when(AST.PrintInstruction)
    def visit(self, node):
        print node.expression.accept(self)

    @when(AST.Operator)
    def visit(self, node):
        left_result = node.leftOperand.accept(self)
        right_result = node.rightOperand.accept(self)

        return operation[node.sign()](left_result, right_result)

    @when(AST.FunDef)
    def visit(self, node):
        self.curScope[ node.id ] = node

    @when(AST.ReturnInstruction)
    def visit(self, node):
        raise ReturnValueException( node.expression.accept(self) )

    @when(AST.FunctionCallOperator)
    def visit(self, node):
        fundef = self.curScope[ node.id ]

        args_dict = {}

        for arg_expr, arg_name in zip( node.arguments, ( arg.id for arg in fundef.args ) ):
            args_dict[ arg_name ] = arg_expr.accept(self)

        self.stack.push( self.curScope )
        self.curScope = ValueScope( self.globalScope )
        for key in args_dict:
            self.curScope[ key ] = args_dict[ key ]

        try:
            fundef.compoundInstructions.accept(self)
        except ReturnValueException as e:
            self.curScope = self.stack.pop()
            return e.value

        # did not found return instruction
        # this situation should not take place if the lack of return instruction have been handled as an semantic error while parsing

        return default_value[ fundef.type.value ]

    @when(AST.CompoundInstructions)
    def visit(self, node):
        node.declarations.accept(self)
        node.instructions.accept(self)


    @when(AST.AssignmentInstruction)
    def visit(self, node):
        self.curScope[ node.id ] = node.expression.accept(self)

    @when(AST.ChoiceInstruction)
    def visit(self, node):
        if node.condition.accept(self) != 0:
            node.instruction.accept(self)


    @when(AST.ChoiceElseInstruction)
    def visit(self, node):
        if node.condition.accept(self):
            node.instruction.accept(self)
        else:
            node.elseInstruction.accept(self)

    @when(AST.WhileInstruction)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.instruction.accept(self)
            except ContinueException:
                pass
            except BreakException:
                break

    @when(AST.RepeatInstruction)
    def visit(self, node):
        while True:
            try:
                node.instructions.accept(self)
            except ContinueException:
                # jump to checking the condition
                pass
            except BreakException:
                break
            # termination condition
            if node.condition.accept(self) == False:
                break

    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()

    @when(AST.BreakInstruction)
    def visit(self, node):
        raise BreakException()

    @when(AST.GroupingOperator)
    def visit(self, node):
        return node.operand.accept(self)