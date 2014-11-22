import collections

def flatten(lst):
	return sum( ([x] if not isinstance(x, list) else flatten(x)
		     for x in lst), [] )


def indent(count, string):
    print "| "*count+str(string)
