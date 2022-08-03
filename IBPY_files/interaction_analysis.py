from .utils import overlapping_dct_from_indices_to_vals

def get_overlapping_segments_ind(lstA, lstB):  
    """Get segments in A and B that overlap.
    
    Args:
        lstA (list of tuples): [(start time, stop time, lab),..].
        lstB (list of tuples): [(start time, stop time, lab),..]
    
    Returns
        dict: {index of segment in lstA: [indices of segments in lstB]}
    """

    indA = 0
    indB = 0
    dct = {}
    while indA < len(lstA) and indB < len(lstB):
        while lstA[indA][0] >= lstB[indB][1]:       
            indB += 1
            if indB >= len(lstB):
                return dct
        while lstA[indA][1] <= lstB[indB][0]:      
            indA += 1
            if indA >= len(lstA):
                return dct
        if (lstA[indA][1] > lstB[indB][1] > lstA[indA][0]) or (
            lstA[indA][1] > lstB[indB][0] > lstA[indA][0]
        ):
            while indB < len(lstB) and lstB[indB][1] < lstA[indA][1]:
                if indA in dct:
                    if indB in dct[indA]:           #added
                        pass                        #added
                    else:                           #added
                      dct[indA].append(indB)
                else:
                    dct[indA] = [indB]
                dct[indA].append(indB+1)            #added
                indB += 1
            indA += 1

        elif (lstB[indB][0] <= lstA[indA][0]) and (lstB[indB][1] >= lstA[indA][1]): 
            while indA < len(lstA) and (lstA[indA][1] < lstB[indB][1]):
                if indA in dct:
                    dct[indA].append(indB)
                else:
                    dct[indA] = [indB]
                indA += 1
            indB += 1

    return dct


def gos_ind(A, B): #get_overlapping_segments_ind - correct function
    """Get segments in A and B that overlap.
    
    Args:
        lstA (list of tuples): [(start time, stop time, lab),..].
        lstB (list of tuples): [(start time, stop time, lab),..]
    
    Returns
        dict: {index of segment in lstA: [indices of segments in lstB]}
    """
    indA = 0
    indB = 0
    dct = {}

    while indA < len(A) and indB < len(B):
        # Left bound for intersecting segment
        l = max(A[indA][0], B[indB][0])
         
        # Right bound for intersecting segment
        r = min(A[indA][1], B[indB][1])
         
        # If segment is valid, we add indices corresponding to A and B to the dictionnary
        if l <= r:
            if indA in dct :            #if A indice is already in the dict,
                dct[indA].append(indB)      #we add B indice to those who are aloready ther
            else :
                dct[indA]=[indB]            
 
        #If the endtime of the i-th interval of list A is smaller, we increment indice A.
        #Else, we increment indice B
        if A[indA][1] < B[indB][1]:
            indA += 1
        else:
            indB += 1

    return dct


def get_overlapping_segments(lstA, lstB, values_only=False):
    """Get segments in lstB overlapping with segments of lstA.
    
    Args:
        lstA ([type]): [(start, stop, label), etc.]
        lstB ([type]): [(start, stop, label), etc.]
        values_only (bool, optional): [description]. Defaults to False.
    
    Returns:
        dict: {Segments in A: [Segments in B]}
    """
    dct_inds = gos_ind(lstA, lstB)
    if values_only:
        lstA_tempo = [val for b, e, val in lstA]
        lstB_tempo = [val for b, e, val in lstB]
    else:
        lstA_tempo = lstA[:]
        lstB_tempo = lstB[:]
    dct = overlapping_dct_from_indices_to_vals(dct_inds, lstA_tempo, lstB_tempo)
    return dct

# high levels
def count_mimicry(lstA, lstB, delta_t=0):
    """Count the occurences of B mimicking A by delta_t.
   
    This implementation counts mimicry based on method in [1]
    and also returns the instances of mimickry.

    The times in each of lstA and lstB cannot overlap internally.
    They have to be successive segments in each of lstA and lstB.

    [1] Feese, Sebastian, et al. "Quantifying behavioral mimicry by automatic 
    detection of nonverbal cues from body motion." 2012 International Conference 
    on Privacy, Security, Risk and Trust and 2012 International Conference on 
    Social Computing. IEEE, 2012.
    
    Args:
        lstA (list): list of tuples (start, stop, label) of expressions mimicked.
        lstB (list): list of tuples (start, stop, label) of expressions mimicking.
        delta_t (int, optional): Defaults to 0.
                                Time after which expression occuring still counts as mimicry.
                                Should be in the same unit as the times in lstA and lstB.    
    Returns:
        int: number of times B mimicked A (=len(the list described below)).
        list: [(indA, indB),...]
              where the indB element of B mimick the indA element of A
              following the definition of mimickry described in the reference above.
    """

    indA = 0
    indB = 0
    count = 0  # number of mimicry events
    mimic_ind = []  # indices of mimicry events in lstB
    if len(lstA) == 0 or len(lstB) == 0:  # if at least one of them has no expression
        return 0, []
    while indA < len(lstA) and indB < len(lstB):
        if lstB[indB][0] <= lstA[indA][0]:
            indB += 1
        elif (
            lstB[indB][0] > lstA[indA][0] and (lstB[indB][0] - delta_t) <= lstA[indA][1]
        ):
            # avoid double counting incase delta_t is > (lstA[indA+1][0] - lstA[indA][1])
            if (indA + 1) < len(lstA):
                if lstB[indB][0] > lstA[indA + 1][0]:
                    indA += 1  # skip to next lstA expression
                    continue
            count += 1
            mimic_ind.append((indA, indB))
            # if no double counting
            # check if several expressions from B overlap with A's
            while lstB[indB][1] <= lstA[indA][1]:
                indB += 1  # skip to the following expression untill no more overlapping
                if indB == len(lstB):
                    break
            indA += 1
        elif (lstB[indB][0] - delta_t) > lstA[indA][1]:
            indA += 1
    return count, mimic_ind


def count_mimicry_per_value_in_tier(ref, target, delta_t):
    """Return the number of times mimicry occured.
    
    Considers that all expresssions in ref and target are the same.
    So all are potential mimicry events.

    Args:
        ref (dict): dictionary of values in tier mimicked.
        target (dict): dictionary of values in tier potentially mimicking.
        delta_t (float): time after which expression occuring still counts as mimicry.
                        Should be in the same unit as the times in ref and target.
    
    Raises:
        AttributeError: [description]
    
    Returns:
        [type]: [description]
    """

    final = {}
    if len(set(ref)) != len(ref):
        raise AttributeError("No parameter is allowed in the parameter ref")
    for r in ref:
        final[r] = {}
        for tar in target:
            final[r][tar] = count_mimicry(ref[r], target[tar], delta_t=delta_t)
    return final


def calculate_mimicking_ratio(total_mimicker_expressions, total_mimicked_expressions):
    """Return the ratio of the total number of expression that are mimicking to 
    the total number of a certain expression.
    
    Args:
        total_mimicker_expr ([type]): [description]
        total_mimicked_expressions ([type]): [description]
    
    Returns:
        [type]: [description]
    """

    return total_mimicked_expressions / total_mimicker_expressions


def following_expressions(lst, delta_t=0):
    """succession of expressions in tier"""
    dct = {}
    for l in range(len(lst) - 1):
        if (lst[l + 1][0] - lst[l][1]) <= delta_t:
            if lst[l][2] in dct:
                dct[lst[l][2]].append(lst[l + 1])
            else:
                dct[lst[l][2]] = [lst[l + 1]]
        else:
            if lst[l][2] in dct:
                dct[lst[l][2]].append(None)
            else:
                dct[lst[l][2]] = [None]
    return dct


def count_vals_in_tier(lst, vals_to_count=None):
    dct = {}
    for lab in lst:
        if lab is not None:
            lab = lab[2]

        if lab in dct:
            dct[lab] += 1
        else:
            dct[lab] = 1
    return dct


def calculate_correlation(lstA, lstB):
    pass #TODO


def count_following(lst, n, max_dist):
    labs = set([l for _, _, l in lst])
    dct = {}
    for l in labs:
        dct[l] = {}
    for i in range(len(lst) - n):
        if lst[i][2] not in dct:
            dct[lst[i][2]] = {}
        if (lst[i + n][0] - lst[i][1]) <= max_dist:
            for j in range(1, n + 1):
                dct[lst[i][2]][j] = {}
                if lst[i + j][2] not in dct[lst[i][2]][j]:
                    dct[lst[i][2]][j][lst[i + j][2]] = 0
                dct[lst[i][2]][j][lst[i + j][2]] += 1
    return dct


def get_next_n_exp(lst, n, max_dist, append_none=True):
    """return lists of n labels following each different label in a list.
    
    Args:
        lst (list of tuples): list of type [(start, stop, label)]
        n (int): number of elements.
        max_dist (int): maximum distance between elements, in number of elements.
                        After this distance, labels are not considered following the current one,
        append_none (bool, optional): fill with None if no more following label. Defaults to True.
    
    Returns:
        dict: {label: [followinglabels]}
    """
    dct = {}
    for l in range(len(lst) - n):  # skip the last n elements (cannot assume they are None)
        lab = lst[l][2]
        if lab not in dct:
            dct[lab] = []
        temp = []
        for ind_next in range(1, n + 1):
            next_close = lst[l + ind_next - 1][1]
            next_far = lst[l + ind_next][0]
            if (next_far - next_close) <= max_dist:
                temp.append(lst[l + ind_next][2])
            else:
                if append_none:
                    temp.extend([None] * (n - ind_next + 1))
                break
        if len(temp) == n:
            dct[lab].append(temp)
    return dct


def get_prev_n_exp(lst, n, max_dist, append_none=True):
    """return lists of n labels preceding each different label in a list.
    
    Args:
        lst (list of tuples): list of type [(start, stop, label)]
        n (int): number of elements.
        max_dist (int): maximum distance between elements, in number of elements.
                        After this distance, labels are not considered preceding the current one,
        append_none (bool, optional): fill with None if no more preceding label. Defaults to True.
    
    Returns:
        dict: {label: [preceding labels]}
    """
    dct = {}
    for l in range(
        n, len(lst)
    ):  # skip the first n elements (cannot assume they are None)
        lab = lst[l][2]
        if lab not in dct:
            dct[lab] = []
        temp = []
        for ind_next in range(1, n + 1):
            prev_close = lst[l - ind_next + 1][0]
            prev_far = lst[l - ind_next][1]
            if (prev_close - prev_far) <= max_dist:
                temp.append(lst[l - ind_next][2])
            else:
                if append_none:
                    temp.extend([None] * (n - ind_next + 1))
                break
        if len(temp) == n:
            dct[lab].append(temp)
    return dct


#ADDED

def get_overlapping_seg(A, B): 
    """Get segments in A and B that overlap.
    Same as get_overlapping_segments but here, the function makes directly intersection between the segments.
    Args:
        lstA (list of tuples): [(start time, stop time, lab),..].
        lstB (list of tuples): [(start time, stop time, lab),..]
    
    Returns
        list: [(startime overlap, endtime overlap, lab)]
    """
    indA = 0
    indB = 0
    lst = []

    while indA < len(A) and indB < len(B):
        # Left bound for intersecting segment
        l = max(A[indA][0], B[indB][0])
         
        # Right bound for intersecting segment
        r = min(A[indA][1], B[indB][1])
         
        # If segment is valid print it
        if l <= r:
            lst.append((l,r,B[indB][2]))
 
        # If i-th interval's right bound is
        # smaller increment i else increment j
        if A[indA][1] < B[indB][1]:
            indA += 1
        else:
            indB += 1

    return lst

