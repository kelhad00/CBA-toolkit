import os
import pympi
from interactionData_transformation import get_overlapping_segments
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

def keep_only(lst, tier_to_keep, inplace = False):
    """ keep filepaths for files with annotation data in the tier tier_to_keep.
    
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
    """ keeps pairs of gst1 and gst2 in lst.
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
    keep = {}
    data = eaf.get_annotation_data_for_tier(tier)
    if values is None:
        values = set([lab for _,_,lab in data])
    for annot in data:
        if annot[2] in values:
            if annot[2] in keep:
                keep[annot[2]].append(annot)
            else:
                keep[annot[2]] = [annot]
    return keep

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