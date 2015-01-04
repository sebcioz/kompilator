#!/usr/bin/python

from collections import defaultdict


class TtypeDict(defaultdict):
    __types = ( "int", "float", "string" )

    def __setitem__(self, index, item):
        if index == "...":
            for type in TtypeDict.__types:
                defaultdict.__setitem__(self, type, item)
        else:
            defaultdict.__setitem__(self, index, item)


class Ttype(object):
    __the_only_one = None
    __created = False
    __defs = \
        """
        int     +   int     =   int
        int     +   float   =   float
        int     +   string  =   _
        float   +   int     =   float
        float   +   float   =   float
        float   +   string  =   _
        string  +   int     =   _
        string  +   float   =   _
        string  +   string  =   string

        int     -   int     =   int
        int     -   float   =   float
        int     -   string  =   _
        float   -   int     =   float
        float   -   float   =   float
        float   -   string  =   _
        string  -   int     =   _
        string  -   float   =   _
        string  -   string  =   _

        int     *   int     =   int
        int     *   float   =   float
        int     *   string  =   _
        float   *   int     =   float
        float   *   float   =   float
        float   *   string  =   _
        string  *   int     =   string
        string  *   float   =   _
        string  *   string  =   _

        int     /   int     =   int
        int     /   float   =   float
        int     /   string  =   _
        float   /   int     =   float
        float   /   float   =   float
        float   /   string  =   _
        string  /   int     =   _
        string  /   float   =   _
        string  /   string  =   _

        ...     %   ...     =   _
        int     %   int     =   int

        ...     |   ...     =   _
        int     |   int     =   int

        ...     &   ...     =   _
        int     &   int     =   int

        ...     ^   ...     =   _
        int     ^   int     =   int

        ...     ||  ...     =   _
        int     ||  int     =   int

        ...     &&  ...     =   _
        int     &&  int     =   int

        ...     >>  ...     =   _
        int     >>  int     =   int

        ...     <<  ...     =   _
        int     <<  int     =   int

        int     ==  int     =   int
        int     ==  float   =   int
        int     ==  string  =   _
        float   ==  int     =   int
        float   ==  float   =   int
        float   ==  string  =   _
        string  ==  int     =   _
        string  ==  float   =   _
        string  ==  string  =   int

        int     !=  int     =   int
        int     !=  float   =   int
        int     !=  string  =   _
        float   !=  int     =   int
        float   !=  float   =   int
        float   !=  string  =   _
        string  !=  int     =   _
        string  !=  float   =   _
        string  !=  string  =   int

        int     >=  int     =   int
        int     >=  float   =   int
        int     >=  string  =   _
        float   >=  int     =   int
        float   >=  float   =   int
        float   >=  string  =   _
        string  >=  int     =   _
        string  >=  float   =   _
        string  >=  string  =   int

        int     <=  int     =   int
        int     <=  float   =   int
        int     <=  string  =   _
        float   <=  int     =   int
        float   <=  float   =   int
        float   <=  string  =   _
        string  <=  int     =   _
        string  <=  float   =   _
        string  <=  string  =   int

        int     <   int     =   int
        int     <   float   =   int
        int     <   string  =   _
        float   <   int     =   int
        float   <   float   =   int
        float   <   string  =   _
        string  <   int     =   _
        string  <   float   =   _
        string  <   string  =   int

        int     >   int     =   int
        int     >   float   =   int
        int     >   string  =   _
        float   >   int     =   int
        float   >   float   =   int
        float   >   string  =   _
        string  >   int     =   _
        string  >   float   =   _
        string  >   string  =   int

        int     =   int     =   int
        int     =   float   =   int
        int     =   string  =   _
        float   =   int     =   float
        float   =   float   =   float
        float   =   string  =   _
        string  =   int     =   _
        string  =   float   =   _
        string  =   string  =   string
        """

    def __new__(cls):
        if Ttype.__the_only_one is None:
            Ttype.__the_only_one = object.__new__(cls)

        return Ttype.__the_only_one

    def __init__(self):
        if not Ttype.__created:
            Ttype.__created = True

            dict_in_dict_factory = lambda: TtypeDict(TtypeDict)
            self.ttype = TtypeDict(dict_in_dict_factory)

            for line in Ttype.__defs.split("\n"):
                if line:
                    (left, op, right, not_used, result) = line.split()
                    self.ttype[op][left][right] = result if result != "_" else None

                    # print self.ttype["%"]

                    # print self.ttype

# a = Ttype()
# b = Ttype()

# print dir(Ttype)

# print a, b
# print a is b
# print id(a), id(b)
