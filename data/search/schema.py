

class Operator(object):
    """ 
    A clause operator, such as equality, less-than/greater-than, or set membership.
    
    Consists of a name and a generator function for mapping arguments to a Django query.
    """

    def __init__(self, param_name, generator):
        self._param_name = param_name
        self._generator = generator
    
    def get_name(self):
        return self._param_name
    
    def apply(self, *args):
        """ Return a Django query """
        return self._generator(*args)


class Field(object):
    """
    A field that may be searched over.
    
    Consists of a name and a set of operators. The search may or may not correlate to a single database field.
    """
    
    def __init__(self, param_name, *operators):
        self._param_name = param_name
        
        self._name_to_op = dict()
        for op in [op for op in operators]:
            self._name_to_op[op.get_name()] = op
            
    def get_op_names(self):
        return self._name_to_op.keys()
    
    def get_op(self, name):
        return self._name_to_op[name]
    
    def get_name(self):
        return self._param_name
    
        
class Schema(object):
    """
    The set of fields that may be used in a query, and the functionality to 
    transform an HTTP request-like object into a Djanog query.
    """
    
    VALUE_DELIMITER = '|'

    def __init__(self, *search_fields):
        self._name_to_field = dict()
        for search_field in search_fields:
            self._name_to_field[search_field.get_name()] = search_field

    def get_field_names(self):
        return self._name_to_field.keys()
    
    def get_field(self, name):
        return self._name_to_field[name]
    
    def get_query_clause(self, field_name, op_name, *values):
        return self.get_field(field_name).get_op(op_name).apply(*values)
    
    def extract_query(self, request):
        """
        Construct a Django query from an HTTP request-like object.
        
        The request should be a dictionary with field name keys (HTTP parameters)
        mapping to strings (HTTP parameter values.) The values should consist of an
        operator name followed by argument values, all separated by a pipe ('|').
        """
        
        def extract_clause(field_name, value):
            value_components = value.split(Schema.VALUE_DELIMITER)
            op_name = value_components[0]
            args = value_components[1:]
            return self.get_query_clause(field_name, op_name, *args)
        
        return [extract_clause(name, value) for (name, value) in request.items()]
        






 

