#!/usr/bin/python

class MultipleDeclarationError(Exception):
    pass

class SymbolScope(object):

    def __init__(self):
        self.parent = None
        self.dict = {}

    def __getitem__(self, id):
        try:
            # return the variable from local scope
            return self.dict[id]
        except KeyError as err:
            if self.parent is not None:
                # return the variable from superior scope
                return self.parent[id]
            else:
                # this is the root scope - variable not found
                raise err

    def __setitem__(self, key, value):
        if key in self.dict:
            raise MultipleDeclarationError( "{0} already declared in this scope".format(key) )
        self.dict[key] = value

    def __str__(self):
        return str(self.dict)

    def keys(self):
        return self.dict.keys()