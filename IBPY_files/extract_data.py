import os
import pympi
import numpy
from os import listdir
from os.path import join
from .processing import tuple_to_sequence


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


def read_eaf_to_dict(filepath, mark=True, tiers=None):
    """Read elan EAF file in a dictionary.
    
    Args:
        filepath ([type]): path to single eaf file
        mark (bool, optional):  append same ID to parent/children tiers.
                                Defaults to True.
        tiers (list): list of tier names to keep and discard the rest.
    
    Returns:
        [dict]: {tier name: [(begin, end, value)]}
    """

    eaf = pympi.Elan.Eaf(filepath)
    dct = {}
    if tiers is None:
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
    """Return a dict of {tier:[(strt, stp, val),...]} if val in values"""   
    eaf = pympi.Elan.Eaf(filepath)
    if values is not None:  # if none keep all
        if not isinstance(values, (list, tuple, numpy.ndarray, str)):
            raise AttributeError("Values must be a list like or a string")
        if isinstance(values, str):
            values = [values]
    dct = {tier:[]}
    data = eaf.get_annotation_data_for_tier(tier)
    if values is None:
        values = set([lab for _, _, lab in data])
    for annot in data:
        if annot[2] in values:
            dct[tier].append(annot)
    return dct


def replace_label(lst, to_replace, value=None, inplace=False, append=None):
    """Replace to_replace label with value in list lst.
    
    Note: Elements of lst should be in the (start time, stop time, label) format.
    """

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
    """Return list not containing the labels in to_remove.
    
    Args:
        lst (list of tuples): list of the type [ ( _, _, label) ] from which data should be removed.
        to_remove (string or list of strings): label(s) that should be removed from lst.
    
    Returns:
        list: list of the same type as lst.
    """

    if isinstance(to_remove, str):
        to_remove = [to_remove]
    newlst = []
    for tup in lst:
        if tup[2] not in to_remove:
            newlst.append(tup)
    return newlst


def keep_only(lst, tier_to_keep, inplace=False):
    """Keep filepaths for files with annotation data in the tier tier_to_keep.

    Note: keep it whether file is entirely annotated or not.
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


#ADDED
def tuple_access(filepath, expression, where, index):
    """
    This function accesses the information of a tuple
    
    Args : 
        filepath (str) --> path of the file
        expression (str) --> Smiles_0 ou Laughs_0
        where (int) --> position of the tuple to which we want to access
        index (int)--> index of the element to be accessed in the tuple (0, 1 ou 2)
    Return : The wanted information
    """
    
    to_dict = read_eaf_to_dict (filepath, mark=True, tiers=None)
    m=to_dict[expression][where-1][index]

    return m

def find_indice_tuple(lst, value, idx):
    """
    Finds the index of a tuple in a list of multiple tuples
    
    Args :
        lst (list) --> the list containing the tuples
        value (int/str) --> value contained in the tuple
        idx (int) --> position in the tuple corresponding to "value"
    Return : 
        int : the index of the tuple where the value at position idx is.
    """
    indice=0
    for _ in lst :
        indice +=1
        if value == _[idx] :
            return (indice)

def get_all_filenames(root, ext, to_fill=None):
    """Return list of eaf files name.
    Args:
        root (str): directory path to read from.
        ext (str): extension of files to read.
        to_fill ([type], optional): list to add the names to. Defaults to None.
                                    If none, considered an empty list.
    Returns:
        [filename1, filname2,....]
    """
    if to_fill is None:
        to_fill = []
    if not isinstance(to_fill, list):
        raise AttributeError("to_fill parameter must be a list")
    paths = os.walk(root)
    for root, _, files in paths:
        #print(root)
        for f in files:
            if f.endswith(ext):
                to_fill.append(os.path.join(f))
    return to_fill
 
def replace_intensity(lst):
    """This function replace intensity by numbers from 1 to 3 or 4.

    Args : lst (list) -> list of tuples (stt, stp, label)

    Return : Return a list with all the labels replaced by numbers
    """

    if "subtle" in [i[2] for i in lst]:
        lst=replace_label(lst, "subtle",value=1)
        lst=replace_label(lst, "low",value=2)
        lst=replace_label(lst, "medium",value=3)
        lst=replace_label(lst, "high",value=4)
    else :
        lst=replace_label(lst, "low",value=1)
        lst=replace_label(lst, "medium",value=2)
        lst=replace_label(lst, "high",value=3)

    return lst

def tuple_to_int_sequence(lst,width, shift):
    """This function convert tuple (stt, stp, label) into a sequence of int corresponding to the label.

    Args:
        lst (list): list of tuple (stt, stp, label)
        width (numeric): window width in ms
        shift (numeric): window shift in ms

    Returns:
        list: A sequence of int
    """
    if len(lst)==0:
        lst_int=[]
    else :
        L=replace_intensity(lst)
        #print(L)
        lst_int=tuple_to_sequence(L,width, shift)
        #print(lst_int)
        for i in range(len(lst_int)) :
            if lst_int[i] is None:
                lst_int[i]=0
    return lst_int

