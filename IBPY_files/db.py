import os
import re

from .utils import list_to_df

from .extract_data import get_all_filenames, get_all_filepaths

# specific db interfaces

## ndc
def form_pairs_ndc(lst):
    """Return filename pairs [(),(),...].

    Args:
        lst (list): list of filenames without the path.

    Returns:
        list: [(),(),...]
    """
    lst_sorted = sorted(lst)
    i = 0
    final = []
    while i <= (len(lst_sorted)-1):
        curr = '_'.join(lst_sorted[i].split('_')[:2])
        nxt = '_'.join(lst_sorted[i+1].split('_')[:2])
        if curr == nxt:
            final.append((lst_sorted[i], lst_sorted[i+1]))
            i+=2
        else:
            # print("File {} has no pair.".format(lst_sorted[i]))
            i+=1
    return final

## ccdb
def form_pairs_ccdb(lst):
    """Return filename pairs [(),(),...].

    Args:
        lst (list): list of filenames without the path.

    Returns:
        list: [(),(),...]
    """

    final = []
    replace_with = {'dizzy':'monk', 'monk':'dizzy'}
    i = 0
    while i < len(lst):
        key = lst[i].split('_')[-1].split('.')[0]
        pair = lst[i].replace(key, replace_with[key])
        if pair in lst:
            final.append((lst[i], pair))
            lst.remove(lst[i])
            lst.remove(pair)
        else:
            # print("File {} has no pair".format(l))
            i=+1
    for l in lst:
        # print("File {} has no pair".format(l))
        continue
    return final

## ifadv
def form_pairs_ifadv(lst):#assuming all have pairs.
    """Return list of filename pairs

    Note: Assuming all elements in lst have pairs.

    Args:
        lst (list): list of filenames.

    Returns:
        list: [(),(),...]
    """
    lst1 = [0] * int(len(lst) / 2)
    lst2 = [0] * int(len(lst) / 2)
    for l in lst:
        ind = int(re.findall("\d+", l)[0])
        if l[2] == "A":
            lst1[ind - 1] = l
        else:
            lst2[ind - 1] = l
    return list(zip(lst1, lst2))

## Place for the user to enter his functions from_pairs_nomDossier 



####

#ADDED
def form_pairs(ROOT1,ROOT2,ROOT3):
    """
    Gives filespath of pairs for each database

    Args:
        ROOT1 (str): path of ccdb directory.
        ROOT2 (str): path of ifadv directory.
        ROOT3 (str): path of ndc directory.        
        
    Returns:
        list: [pair1_A, pair1_B, pair2_A, pair2_B,....]

    """
    c=form_pairs_ccdb(get_all_filenames(ROOT1,"eaf"))
    i=form_pairs_ifadv(get_all_filenames(ROOT2,"eaf"))
    n=form_pairs_ndc(get_all_filenames(ROOT3, "eaf"))
    liste_ccdb = list(sum(c, ())) 
    liste_ifadv = list(sum(i, ())) 
    liste_ndc = list(sum(n, ())) 
    
    pair_ccdb, pair_ifadv, pair_ndc=([] for _ in range(3))
    for _ in liste_ccdb:
        pair_ccdb.append(ROOT1+f"\{_}")
    for _ in liste_ifadv:
        pair_ifadv.append(ROOT2+f"\{_}")
    for _ in liste_ndc:
        pair_ndc.append(ROOT3+f"\{_}")

    return (pair_ccdb, pair_ifadv, pair_ndc)

def form_list_pairs_ccdb(ROOT1):
    """
    Gives filespath of pairs for ccdb database
    
    Args:
        ROOT1 (str): path of ccdb directory.

    Returns:
        list: [pair1_A, pair1_B, pair2_A, pair2_B,....]

    """
    c=form_pairs_ccdb(get_all_filenames(ROOT1,"eaf"))
    liste_ccdb = list(sum(c, ())) 
    pair_ccdb=[]
    for _ in liste_ccdb:
        pair_ccdb.append(ROOT1+f"\{_}")
    return pair_ccdb

def form_list_pairs_ifadv(ROOT2):
    """
    Gives filespath of pairs for ifadv database

    Args:
        ROOT1 (str): path of ifadv directory.

    Returns:
        list: [pair1_A, pair1_B, pair2_A, pair2_B,....]

    """
    i=form_pairs_ifadv(get_all_filenames(ROOT2,"eaf"))
    liste_ifadv = list(sum(i, ())) 
    pair_ifadv=[]
    for _ in liste_ifadv:
        pair_ifadv.append(ROOT2+f"\{_}")
    return pair_ifadv

def form_list_pairs_ndc(ROOT3):
    """
    Gives filespath of pairs for ndc database
    
    Args:
        ROOT1 (str): path of ndc directory.

    Returns:
        list: [pair1_A, pair1_B, pair2_A, pair2_B,....]
    """
    n=form_pairs_ndc(get_all_filenames(ROOT3, "eaf"))
    liste_ndc = list(sum(n, ())) 
    pair_ndc=[]
    for _ in liste_ndc:
        pair_ndc.append(ROOT3+f"\{_}")
    return pair_ndc

def get_db_from_func_pair(dir, func):
    """This function takes a path as an argument and creates a database 
        based on the number of items in the folder using a chosen function.
    It takes into account pairs in our databases.

    Args:
        dir (str) : path of the folder containing all databases.
        func (function): Function we want to use.

    Returns:
        dataframe: A dataframe corresponding to the function chosen
    """
    n=0
    L=[]
    dct={"ccdb":form_list_pairs_ccdb, "ifadv":form_list_pairs_ifadv, "ndc":form_list_pairs_ndc}
    for path in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, path)):
            n+=1
            for i,j in zip (list(dct.keys()), list(dct.values())):
                if path==i:
                    L.append((j(os.path.join(dir, path)), path))
            # if path == "ccdb":
            #     L.append((form_list_pairs_ccdb(os.path.join(DIR, path)), path))
            # if path == "ifadv":
            #     L.append((form_list_pairs_ifadv(os.path.join(DIR, path)), path))
            # if path == "ndc":
            #     L.append((form_list_pairs_ndc(os.path.join(DIR, path)), path))
    dg=[]
    for i in range (len(L)) :
        dg+=func(L[i][0], L[i][1])[0]

    dg=list_to_df(dg, func(L[0][0], L[0][1])[1])
    return dg

def get_db_from_func_no_pair(dir, func):
    """This function takes a path as an argument and creates a database 
        based on the number of items in the folder using a chosen function.
    It doesn't take into account pairs in our databases.

    Args:
        dir (str) : path of the folder containing all databases.
        func (function): Function we want to use.

    Returns:
        dataframe: A dataframe corresponding to the function chosen
    """
    n=0
    L=[]
    for path in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, path)):
            n+=1
            data=["ccdb","ifadv","ndc"]
            for i in data:
                if path==i:
                    L.append((get_all_filepaths((os.path.join(dir, path)), "eaf", None) , path))

    dg=[]
    for i in range (len(L)) :
        dg+=func(L[i][0], L[i][1])[0]

    
    dg=list_to_df(dg, func(L[0][0], L[0][1])[1])
    return dg

