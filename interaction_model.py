class Expressions:
    """Represent the expressions of a subject
    """

    def __init__(self, expr_dct):
        """ expr_dct (dict): {expression name:value} """ 
        self.add_expr(expr_dct)

    def add_expr(self, dct):
        for l, val in dct.items():
            setattr(self, "_" + l, val)
            setattr(self, l, property(self.getter("_" + l), self.setter("_" + l, val)))
            setattr(self, l, val)

    def getter(self, attr):
        # add condition if needed
        return getattr(self, attr)

    def setter(self, attr, val):
        # add condition if needed
        return setattr(self, attr, val)

    @property
    def expr(self):
        """Get list of expressions"""
        lst = [l for l in self.__dict__ if not l.startswith("_")]
        return lst


class Subject:
    """Represent an individual."""
    def __init__(self, subj_id, expr=None):
        self.id = subj_id
        if expr is not None:
            if not isinstance(expr, Expressions):
                raise AttributeError(
                    "expr must be of type {}".format(Expressions.__name__)
                )


class Interaction:
    """Represent an interaction."""
    def __init__(self, subj_lst):
        if not isinstance(subj_lst, (list, tuple)):  # is list
            raise AttributeError("sub_lst must be a list or tuple")
        for subj in subj_lst:
            if not isinstance(subj, Subject):  # is Subject
                raise AttributeError("Input must be of type {}".format(Subject.__name))
            setattr(self, subj)  # add to attributes
