import os
import re

# interfaces
# iteract with the different databases

## ent17
def get_pairs_ent17(path):
    """return list of annotation file pairs"""
    lst = os.listdir(path)
    lst = [l for l in lst if l.endswith(".eaf")]
    lst1 = [0] * int(len(lst) / 2)
    lst2 = [0] * int(len(lst) / 2)
    for l in lst:
        ind = int(l.split("_")[-1].split(".")[0])
        if l.startswith("MVI_1"):
            lst1[ind] = l
        else:
            lst2[ind] = l
    return list(zip(lst1, lst2))


## ccdb
def get_pairs_ccdb(path):
    """return list of annotation file pairs"""
    lst = os.listdir(path)
    lst = [l for l in lst if l.endswith(".eaf")]
    lst.sort()
    final = []
    for i in range(0, int(len(lst) / 2), 2):
        final.append((lst[i], lst[i + 1]))
    return final


## ifadv
def get_pairs_ifadv(path):
    """return list of annotation file pairs"""
    lst = os.listdir(path)
    lst = [l for l in lst if l.endswith(".eaf")]
    lst1 = [0] * int(len(lst) / 2)
    lst2 = [0] * int(len(lst) / 2)
    for l in lst:
        ind = int(re.findall("\d+", l)[0])
        if l[2] == "A":
            lst1[ind - 1] = l
        else:
            lst2[ind - 1] = l
    return list(zip(lst1, lst2))
