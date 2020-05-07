from CBA.interaction_analysis import *
from CBA.utils import AttributeGenerator

class Expression:

    def __init__(self, name, val):
        """we don't know if val is ordered or not"""
        self.name = name
        self.val = val
    
    def replace_label(self, old, new):
        """Return list of (strt, stp, lab) with the old labels replaces by new."""
        if not isinstance(old, (list, tuple)):
            old = [old]
        if hasattr(old, '__iter__') and not isinstance(old, (list, tuple)):
            raise AttributeError('old must be a str, list or tuple')
        new_lst = [(strt, stp, new)  if l in old else (strt, stp, l) for (strt, stp, l) in self.val]
        return new_lst

    def get_duration(self):
        """considering that the list is unordered."""
        last = self.val[-1][2]
        for strt, stp, lab in self.val[-2::-1]:
            if stp <= last:
                break
            else:
                last = stp
        return last

    def label_count(self):
        """Return dictionnary of labels count."""
        dct = {}
        for _,_,lab in self.val:
            if lab not in cnt_dct:
                cnt_dct[lab] = 0
            else:
                cnt_dct[lab]+=1
        return cnt_dct

    def overlap_with(self, lst):
        dct = get_overlapping_segments(self,val, lst)
        return dct
        
class Subject(AttributeGenerator):
    """Represent an individual."""
    def __init__(self, subj_id, expr=None):
        self.id = subj_id
        self.add_expr(expr)

    def add_expr(self, expr):
        """Add expression to Subject instance."""
        if expr is not None:
            if isinstance(expr, Expression):
                expr = [expr]
            if not isinstance(expr, list):
                raise AttributeError('expr must be of type {} or list of {}'.format(Expression.__name__))
            for x in expr:
                super()._add(x.name, x.val)
    
    @property
    def expr_lst(self):
        """Return a list of expressions added."""
        return super()._list_attr

class Interaction:
    """Represent an interaction."""
    def __init__(self, subj_lst):
        if not isinstance(subj_lst, (list, tuple)):  # is list
            raise AttributeError("sub_lst must be a list or tuple")
        for subj in subj_lst:
            if not isinstance(subj, Subject):  # is Subject
                raise AttributeError("Input must be of type {}".format(Subject.__name))
            setattr(self, subj)  # add to attributes
