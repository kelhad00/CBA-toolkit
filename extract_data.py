import os
import pympi
import numpy

def get_all_filepaths(root, ext, to_fill=None):
    """Return list of eaf files.
    
    Args:
        root (str): directory path to read from.
        ext (str): extension of files to read.
        to_fill ([type], optional): list to add the paths to. Defaults to None.
                                    If none, considered an empty list.
    
    Returns:
        [type]: [description]
    """
    
    if to_fill is None:
        to_fill = []
    if not isinstance(to_fill, list):
        raise AttributeError("to_fill parameter must be a list")
    paths = os.walk(root)
    for root, _, files in paths:
        for f in files:
            if f.endswith(ext):
                to_fill.append(os.path.join(root, f))
    return to_fill


def read_eaf_to_dict(filepath, mark=True):
    """Read elan EAF file in a dictionary.
    
    Args:
        filepath ([type]): path to single eaf file
        mark (bool, optional):  append same it to parent/children tiers.
                                Defaults to True.
    
    Returns:
        [dict]: {tier name: [(begin, end, value)]}
    """
    eaf = pympi.Elan.Eaf(filepath)
    dct = {}
    tiers = list(eaf.get_tier_names())
    if mark:  # mark parents and children tiers with same ID
        # get parents and children
        par_child_dct = {}
        for tier in tiers:
            param = eaf.get_parameters_for_tier(tier)
            try:  # parents exist
                if param["PARENT_REF"] not in par_child_dct:
                    par_child_dct[param["PARENT_REF"]] = [tier]
                else:
                    par_child_dct[param["PARENT_REF"]].append(tier)
            except:  # no parents
                continue
        par_child_id = 0
        for parent in par_child_dct:
            for t in range(len(tiers)):
                if (tiers[t] in parent) or (tiers[t] in par_child_dct[parent]):
                    tiers[t] = "_".join([tiers[t], str(par_child_id)])
            par_child_id += 1
    # create final dct
    for tier in tiers:
        dct[tier] = eaf.get_annotation_data_for_tier(tier.split("_")[0])
    return dct

def get_tier_from_file(filepath, tier, values=None):
    """Return a dict of {value:[(strt, stp, val),...]} """
    eaf = pympi.Elan.Eaf(filepath)
    if values is not None:  # if none keep all
        if not isinstance(values, (list, tuple, numpy.ndarray, str)):
            raise AttributeError("Values must be a list like or a string")
        if isinstance(values, str):
            values = [values]
    dct = {}
    data = eaf.get_annotation_data_for_tier(tier)
    if values is None:
        values = set([lab for _, _, lab in data])
    for annot in data:
        if annot[2] in values:
            if annot[2] in dct:
                dct[annot[2]].append(annot)
            else:
                dct[annot[2]] = [annot]
    return dct

def keep_pairs(paths_lst, pattern1, pattern2):
    """Keeps pairs of pattern1 and patterns in paths_lst.
    The paths that do not have pairs are not kept.
    """

    ref = set(paths_lst)
    pairs = []
    for l in paths_lst:
        if os.path.basename(l).split("_")[1] == pattern1:
            if l.replace(pattern1, pattern2) in ref:
                pairs.extend([l, l.replace(pattern1, pattern2)])
    return pairs

def replace_label(lst, to_replace, value=None, inplace=False, append=None):
    """Replace to_replace label with value in list lst.
    
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
                value = "_".join([newlst[l][2], append])
            newlst[l] = newlst[l][0], newlst[l][1], value
    return newlst


def remove_label(lst, to_remove):
    """Return new list without elements containing to_remove labels.
    
    Elements of lst should be in the (start time, stop time, label) format."""

    if isinstance(to_remove, str):
        to_remove = [to_remove]
    newlst = lst[:]
    ind = 0
    while ind < len(newlst):
        if newlst[ind][2] in to_remove:
            newlst.pop(ind)
            ind -= 1
        ind += 1
    return newlst


def keep_only(lst, tier_to_keep, inplace=False):
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
        each_tier_content = [
            len(eaf.get_annotation_data_for_tier(tier)) == 0 for tier in tier_to_keep
        ]
        if any(each_tier_content):
            filter_lst.pop(i)
            limit -= 1
            continue
        i += 1
    return filter_lst

