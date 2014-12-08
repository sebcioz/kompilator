#!/usr/bin/python

from node_visitor import NodeVisitor
from collections import defaultdict
from errors import ErrorMsg, WarningMsg
import AST
from itertools import izip_longest

class TypeChecker(NodeVisitor):

    def __init__(self):
        NodeVisitor.__init__(self)