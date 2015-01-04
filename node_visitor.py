#!/usr/bin/python

import AST


class NodeVisitor(object):
    def __init__(self):
        self.errors = []
        self.warnings = []

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        parent_method = 'visit_' + node.__class__.__bases__[0].__name__

        visitor = getattr(self, method, None)
        if visitor is None:
            visitor = getattr(self, parent_method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

                    # simpler version of generic_visit, not so general
                    # def generic_visit(self, node):
                    #    for child in node.children:
                    #        self.visit(child)
