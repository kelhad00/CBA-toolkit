def count_mimicry(tA, tB, delta_t=0):
    """Count the occurences of B mimicking A by delta_t.

    The times in each of tA and tB cannot overlap internally.
    They have to be successive segments in each of tA and tB
    count mimicry events of tB on tA.
    delta_t is only to condition the start border of the tB
    
    This implementation counts mimicry based on method in [1].

    [1] Feese, Sebastian, et al. "Quantifying behavioral mimicry by automatic 
    detection of nonverbal cues from body motion." 2012 International Conference 
    on Privacy, Security, Risk and Trust and 2012 International Conference on 
    Social Computing. IEEE, 2012.
    
    Args:
        tA (list): list of tuples (start time, stop time, label) of expressions mimicked.
        tB (list): list of tuples (start time, stop time, label) of expressions mimicking.
        delta_t (int, optional): Defaults to 0.
                                Time after which expression occuring still counts as mimicry.
                                Should be in the same unit as the times in tA and tB.    
    Returns:
        int: number of times B mimicked A.
    """

    indA = 0
    indB = 0
    count = 0
    while (indA<len(tA) and indB<len(tB)):
        if tB[indB][0]<=tA[indA][0]:
            indB+=1
        elif (tB[indB][0]>tA[indA][0] and (tB[indB][0]-delta_t)<=tA[indA][1]):
            #avoid double counting incase delta_t is > (tA[indA+1][0] - tA[indA][1])
            if (indA+1)<len(tA):
                if tB[indB][0]>tA[indA+1][0]:
                    indA+=1#skip to next tA expression
                    continue
            #if no double counting
            #check if several expressions from B overlap with A's
            while tB[indB][1]<=tA[indA][1]:
                indB+=1 #skip to the following expression untill no more overlapping
                if indB == len(tB):
                    break
            count+=1
            indA+=1
        elif ((tB[indB][0]-delta_t)>tA[indA][1]):
            indA+=1
    return count

def count_mimicry_per_value_in_tier(ref, target, delta_t):
    """Returns the number of times mimicry occured.
    
    Considers that all expresssions in ref and target are the same.
    So all are potential mimicry events.

    Args:
        ref (dict): dictionary of values in tier begin mimicked.
        target (dict): dictionary of values in tier containing mimicry events.
        delta_t (float): time after which expression occuring still counts as mimicry.
                        Should be in the same unit as the times in ref and target.
    
    Raises:
        AttributeError: [description]
    
    Returns:
        [type]: [description]
    """

    final = {}
    if len(set(ref))!= len(ref):
        raise AttributeError("No parameter is allowed in the parameter ref")
    for r in ref:
        final[r] = {}
        for tar in target:
            final[r][tar] = count_mimicry(ref[r], target[tar], delta_t = delta_t)
    return final

def following_expressions(lst, delta_t=0):
    """succession of expressions in tier"""
    dct = {}
    for l in range(len(lst)-1):
        if (lst[l+1][0] - lst[l][1]) <= delta_t:
            if lst[l][2] in dct:
                dct[lst[l][2]].append(lst[l+1])
            else:
                dct[lst[l][2]] = [lst[l+1]]
        else:
            if lst[l][2] in dct:
                dct[lst[l][2]].append(None)
            else:
                dct[lst[l][2]] = [None]
    return dct

def count_vals_in_tier(lst, vals_to_count = None):
    dct = {}
    for lab in lst:
        if lab is not None:
            lab = lab[2]
        
        if lab in dct:
            dct[lab]+=1
        else:
            dct[lab]=1
    return dct