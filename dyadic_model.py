class Expressions():
    """Represents the expressions of a subject
    """
    def __init__(self, dct):
        self.add_expr(dct)

    def add_expr(self, lst):
        for l, val in lst.items():
            setattr(self, '_'+l, val)
            setattr(self, l, property(self.getter('_'+l), self.setter('_'+l, val)))
            setattr(self, l, val)

    def getter(self, attr):
        #add condition if needed
        return getattr(self, attr)

    def setter(self, attr, val):
        #add condition if needed
        return setattr(self, attr, val)

    @property
    def expr(self):
        """Get list of expressions"""
        lst = [l for l in self.__dict__ if not l.startswith('_')]
        return lst

class Subject():
    """Represents a single interaction participant.
    """
    def __init__(self, subj_id, expr=None):
        self.id = subj_id
        if expr is not None:
            if not isinstance(expr, dict):
                raise AttributeError("expr_dct not dict")


class Interaction():
    """Represents an interaction
    """
    def __init__(self, subj):
        if not isinstance(subj, (list, tuple)):#is list
            raise AttributeError("sub_lst must be a list or tuple")
        for subj in subj_lst:
            if not isinstance(subj, Subject):#is Subject
                raise AttributeError("Input must be of type {}".format(type(Subject)))
            setattr(self, subj)#add to attributes
    