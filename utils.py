import os
import pympi
import numpy
import shelve
from interaction_analysis import *
from visualization import gantt

def get_all_eaf_files(root = ".", to_fill = None):
    """return list of eaf files.
        root (str, optional): Defaults to ".". [description]
        to_fill (list, optional): Defaults to []. [description]
    """
    if to_fill is None:
        to_fill = []
    paths = os.walk(root)
    for root, _, files in paths:
        for f in files:
            if f.endswith(".eaf"):
                to_fill.append(os.path.join(root,f))
    return to_fill

def extend_list(lst):
    """[ [], [], []... ] -> []"""

    return [l for sublst in lst for l in sublst]

def extend_dict(dct):
    """{k1:v1, k2:v2, ...} -> [v1, v2, ...] """

    return [l for k in dct for l in dct[l]]

def replace_label(lst, to_replace, value=None, inplace=False, append=None):
    """replace to_replace label with value in list lst.
    
    Elements of lst should be in the (start time, stop time, label) format."""

    if not (value or append):
        raise AttributeError("both value and append parameters cannot be None.")
    if isinstance(to_replace, str):
        to_replace = [to_replace]
    if not inplace:
        newlst = lst[:]
    for l in range(len(newlst)):
        if newlst[l][2] in to_replace:
            if append:
                value = "_".join([newlst[l][2],append])
            newlst[l] = newlst[l][0], newlst[l][1], value
    return newlst

def remove_label(lst, to_remove):
    """return new list without elements containing to_remove labels.
    
    Elements of lst should be in the (start time, stop time, label) format."""

    if isinstance(to_remove, str):
        to_remove = [to_remove]
    newlst = lst[:]
    ind = 0
    while ind<len(newlst):
        if newlst[ind][2] in to_remove:
            newlst.pop(ind)
            ind-=1
        ind+=1
    return newlst

def keep_only(lst, tier_to_keep, inplace = False):
    """Keep filepaths for files with annotation data in the tier tier_to_keep.
    
    Note: should not be used when annotations are complete of the tiers of interst.
    """
    if inplace:
        filter_lst = lst
    else:
        filter_lst = lst[:]
    i = 0
    limit = len(filter_lst)
    while i < limit:
        eaf = pympi.Elan.Eaf(filter_lst[i])
        each_tier_content = [len(eaf.get_annotation_data_for_tier(tier)) == 0 for tier in tier_to_keep]
        if any(each_tier_content):
            filter_lst.pop(i)
            limit-=1
            continue
        i+=1
    return filter_lst

def keep_pairs(lst):
    """Keeps pairs of gst1 and gst2 in lst.
    The paths that do not have pairs are not kept.
    """

    ref = set(lst)
    pairs = []
    for l in lst:
        if os.path.basename(l).split('_')[1] == 'gst1':
            if l.replace('gst1', 'gst2') in ref:
                pairs.extend([l, l.replace('gst1', 'gst2')]) 
    return pairs

def get_tier_val(filepath, tier, values=None):
    """return a dict of {value:[(start, stop, label),...]} with the values in the tier of the eaf"""
    eaf = pympi.Elan.Eaf(filepath)
    if values is not None:#if none keep all
        if not isinstance(values, (list, tuple, numpy.ndarray, str)):
            raise AttributeError("Values must be a list like or a string")
        if isinstance(values, str):
            values = [values]
    dct = {}
    data = eaf.get_annotation_data_for_tier(tier)
    if values is None:
        values = set([lab for _,_,lab in data])
    for annot in data:
        if annot[2] in values:
            if annot[2] in dct:
                dct[annot[2]].append(annot)
            else:
                dct[annot[2]] = [annot]
    return dct

def get_tier(filepath, tiers):
    """Return values of all tiers in eaf file.
    
    Args:
        filepath (str): path to an eaf file
        tiers (list-like of str): tier name or list of tier names
    
    Raises:
        AttributeError: parameter types not respected.
    
    Returns:
        dict: {tier name: tier content}
    """

    eaf = pympi.Elan.Eaf(filepath)
    if not isinstance(tiers, (list, tuple, numpy.ndarray, str)):
        raise AttributeError("tier should be a string or a list-like of strings")
    elif isinstance(tiers, str):
        return eaf.get_annotation_data_for_tier(tiers)
    dct = {}
    for tier in tiers:
        dct[tier] = eaf.get_annotation_data_for_tier(tier)
    return dct

def get_overlapping_segments(lstA, lstB):
    """get segments in A and B that overlap.
    
    Note: example lstA Roles lstB S&L
    
    Args:
        lstA (list of tuples): [(start time, stop time, lab),..].
        lstB (list of tuples): [(start time, stop time, lab),..]
    
    Returns
        dict: {index of segment in lstA: [indices of segments in lstB]}
    """

    indA = 0
    indB = 0
    dct = {}
    while indA<len(lstA) and indB<len(lstB):
        while lstA[indA][0]>=lstB[indB][1]:
            indB+=1
            if indB>=len(lstB):
                return dct
        while lstA[indA][1]<=lstB[indB][0]:
            indA+=1
            if indA>=len(lstA):
                return dct
        if (lstA[indA][1]>lstB[indB][1]>lstA[indA][0]) or (lstA[indA][1]>lstB[indB][0]>lstA[indA][0]):
            while indB<len(lstB) and lstB[indB][1]<lstA[indA][1]:
                if indA in dct:
                    dct[indA].append(indB)
                else:
                    dct[indA] = [indB]
                indB+=1
            indA+=1
        elif (lstB[indB][0]<=lstA[indA][0]) and (lstB[indB][1]>=lstA[indA][1]):
            while indA<len(lstA) and lstA[indA][1]<lstB[indB][1]:
                if indA in dct:
                    dct[indA].append(indB)
                else:
                    dct[indA] = [indB]
                indA+=1
            indB+=1
    return dct

def convert_overlapping_dct_from_indices_to_vals(dct_inds, lstA, lstB):
    """lstA and lstB are lists of labels only and not [(),(), etc.]"""

    dct_vals = {}
    for indA, B in dct_inds.items():
        dct_vals[lstA[indA]] = [lstB[indB] for indB in B]
    return dct_vals

def save_to_shelve(filename, data_name, data, flag='n'):
    with shelve.open(filename, flag) as f:
        f[data_name] = data
    return