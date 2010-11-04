# note: don't really want 

def cross(l, *rest):
    """ Return the cross product of lists. """
    if not rest:
        return [[x] for x in l]
    return [[x] + y for x in l for y in cross(rest[0], *rest[1:])]


def cross_calls(methods, *arg_lists):
    """ Return a list of all methods on all argument combinations.
    
        Each returned item is a pair of string label and function.
        The functions are not bound to an instance--they expect self as the only argument.
        
    """
    def bind(method, args):
        return lambda api: method(api, *args)
    
    result = []
    for call in cross(methods, *arg_lists):
        method = call[0]
        args = call[1:]
        label = "%s(%s)" % (method.__name__, ", ".join(map(str, args)))
        func = bind(method, args)
        result.append((label, func))

    return result

