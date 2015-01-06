#!/usr/bin/python

from node_visitor import NodeVisitor
from collections import defaultdict
from errors import ErrorMsg, WarningMsg
import AST
from itertools import izip_longest
from ttype import Ttype


class TypeChecker(NodeVisitor):
    def __init__(self):
        NodeVisitor.__init__(self)
        self.ttype = Ttype().ttype
        self.arg_reaction = defaultdict(dict)

        self.__init_arg_reactions()


    def visit_AssignmentInstruction(self, node):
        assignment_type = self.visit(node.id)
        expr_type = self.visit(node.expression)

        try:
            result_type = self.ttype["="][assignment_type][expr_type]
            if result_type is None:
                self.errors.append(ErrorMsg("Cannot assign {1} to {0}".format(assignment_type, expr_type), node.line))

            return result_type
        except KeyError:
            # if operands are valid
            if assignment_type is not None and expr_type is not None:
                # unfortunately forgot to define result type for this operation - assume that is an invalid operation
                self.errors.append(ErrorMsg("Cannot assign {1} to {0}".format(assignment_type, expr_type), node.line))

            return None

    def visit_Declaration(self, node):
        id_type = node.id.type.value
        value_type = self.visit(node.value)

        try:
            result_type = self.ttype["="][id_type][value_type]

            if result_type is None:
                self.errors.append(ErrorMsg("Cannot assign {1} to {0}".format(id_type, value_type), node.line))

            return result_type
        except KeyError:
            # if operands are valid
            if id_type is not None and value_type is not None:
                # unfortunately forgot to define result type for this operation - assume that is an invalid operation
                self.errors.append(ErrorMsg("Cannot assign {1} to {0}".format(id_type, value_type), node.line))

            return None


    def visit_Operator(self, node):
        left_type = self.visit(node.leftOperand)
        right_type = self.visit(node.rightOperand)

        try:
            result_type = self.ttype[node.sign()][left_type][right_type]
            if result_type is None:
                self.errors.append(
                    ErrorMsg("Cannot [{1} {0} {2}]".format(node.sign(), left_type, right_type), node.line))

            return result_type
        except KeyError:
            if left_type is not None and right_type is not None:
                self.errors.append(
                    ErrorMsg("Cannot [{1} {0} {2}]".format(node.sign(), left_type, right_type), node.line))

            return None

    def visit_FunctionCallOperator(self, node):
        funDef = node.scope[node.id]
        funName = node.id

        if not isinstance(funDef, AST.FunDef):
            self.errors.append(ErrorMsg("Identifier {0} does not name a function".format(funName), node.line))
            return None

        for expected_arg, given_arg in izip_longest(funDef.args, node.arguments):
            if expected_arg is None:
                self.errors.append(ErrorMsg("Provided too many parameters to function {0}".format(funName), node.line))
                return None

            if given_arg is None:
                self.errors.append(
                    ErrorMsg("Provided not enough parameters to function {0}".format(funName), node.line))
                return None

            expected_type = expected_arg.type.value
            given_type = self.visit(given_arg)

            self.arg_reaction[expected_type][given_type](node.id, expected_arg.id.value, expected_type, given_type,
                                                         node.line)

        return self.visit(node.id)


    def visit_ReturnInstruction(self, node):
        # find parent func def
        parentFunc = node
        while not isinstance(parentFunc, AST.FunDef):
            parentFunc = parentFunc.parent
            if parentFunc is None:
                self.errors.append(ErrorMsg("Return outside function body", node.line))
                return None

        got_type = self.visit(node.expression)
        expected_type = parentFunc.type.value

        if expected_type != got_type:
            self.errors.append(
                ErrorMsg("Invalid return type {0}. Expected {1}".format(got_type, expected_type), node.line))

    def visit_ID(self, node):
        keys = node.scope.keys()
        originKeys = filter(lambda key: key == node, keys)

        if len(originKeys) == 0:
            return None

        return originKeys[0].type.value

    def visit_GroupingOperator(self, node):
        return self.visit(node.operand)

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'


    # TypeChecker help functions
    def __error(self, func_name, arg_name, expected, given, line):
        self.errors.append(ErrorMsg(
            "Function {} expects parameter {} as {}. {} given instead".format(func_name, arg_name, expected, given),
            line))

    def __warning(self, func_name, arg_name, expected, given, line):
        self.warnings.append(WarningMsg(
            "Function {} expects parameter {} as {}. Implicit casting from {}".format(func_name, arg_name, expected,
                                                                                      given), line))

    def __cool(self, func_name, arg_name, expected, given, line):
        pass

    def __init_arg_reactions(self):
        # first dict - expected type; sub-dict - given type
        self.arg_reaction["int"]["int"] = self.__cool
        self.arg_reaction["int"]["float"] = self.__warning
        self.arg_reaction["int"]["string"] = self.__error

        self.arg_reaction["float"]["int"] = self.__cool
        self.arg_reaction["float"]["float"] = self.__cool
        self.arg_reaction["float"]["string"] = self.__error

        self.arg_reaction["string"]["int"] = self.__error
        self.arg_reaction["string"]["float"] = self.__error
        self.arg_reaction["string"]["string"] = self.__cool