

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
    
    Consists of a name and an apply method. The search may or may not correlate to a single database field.
    """
    
    def __init__(self, name):
        self._name = name
            
    def get_name(self):
        return self._name

    def apply(self, args):
        raise NotImplementedError
    
    
class OperatorField(Field):
    """
    A field that support multiple operators.
    
    The first argument to the apply method should always be the operator name.
    """
            
    def __init__(self, name, *operators):
        super(OperatorField, self).__init__(name)
        
        self._name_to_op = dict()
        for op in [op for op in operators]:
            self._name_to_op[op.get_name()] = op
            
    def apply(self, op_name, *args):
        return self._name_to_op[op_name].apply(*args)
    
class InclusionField(Field):
    """
    A field where the only operation is inclusion.
    
    The arguments to apply should be a delimited list of values.
    """
    
    def __init__(self, name, inclusion_op):
        super(InclusionField, self).__init__(name)
        self._inclusion_op = inclusion_op
      
    def apply(self, *args):
        return self._inclusion_op(*args)
        
        
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
    
    def _apply(self, field_name, value):
        args = value.split(Schema.VALUE_DELIMITER)
        return self.get_field(field_name).apply(*args)
    
    def extract_query(self, request):
        """
        Construct a Django query from an HTTP request-like object.
        
        The request should be a dictionary with field name keys (HTTP parameters)
        mapping to strings (HTTP parameter values.) The values should consist of an
        operator name followed by argument values, all separated by a pipe ('|').
        """
        
        return [self._apply(name, value) for (name, value) in request.iteritems()]
        






 

