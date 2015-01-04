#!/usr/bin/python

from node_visitor import NodeVisitor
import scope
from errors import ErrorMsg


class VisibilityChecker(NodeVisitor):
    def __init__(self):
        NodeVisitor.__init__(self)

    def visit_Declaration(self, node):
        try:
            node.scope[node.id] = node.value
            self.visit(node.value)
        except scope.MultipleDeclarationError:
            self.errors.append(ErrorMsg("Multiple declaration of {0}".format(node.id.value), node.line, node.column))

    def visit_ID(self, node):
        try:
            return node.scope[node]
        except KeyError:
            self.errors.append(
                ErrorMsg("{0} not declared in this scope".format(node.value), node.parent.line, node.parent.column))


    def visit_FunDef(self, node):
        try:
            node.parent.scope[node.id] = node
        except scope.MultipleDeclarationError:
            self.errors.append(ErrorMsg("Multiple declaration of {0}".format(node.id.value), node.line, node.column))

        # fill its own scope with arg list (this scope is shared with body compound instruction)
        for arg in node.args:
            try:
                node.scope[arg.id] = arg.type.value
            except scope.MultipleDeclarationError:
                self.errors.append(ErrorMsg(
                    "Multiple declaration of parameter {0} in function {1}".format(arg.id.value, node.id.value),
                    node.line, node.column))

        self.visit(node.compoundInstructions)

    def visit_FunctionCallOperator(self, node):

        try:
            node.scope[node.id]
        except KeyError:
            self.errors.append(ErrorMsg("{0} not declared in this scope".format(node.id.value), node.line, node.column))

        for arg in node.arguments:
            self.visit(arg)

    def visit_AssignmentInstruction(self, node):
        try:
            node.scope[node.id]
        except KeyError:
            self.errors.append(ErrorMsg("{0} not declared in this scope".format(node.id.value), node.line, node.column))
        self.visit(node.expression)
