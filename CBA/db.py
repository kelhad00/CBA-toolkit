import os
import re

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
            print("File {} has no pair.".format(lst_sorted[i]))
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
            print("File {} has no pair".format(l))
            i=+1
    for l in lst:
        print("File {} has no pair".format(l))
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