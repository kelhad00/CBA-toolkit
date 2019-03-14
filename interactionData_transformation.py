def levels_to_numeric(lst, dct = None, return_levels_only=False):
    """returns numeric version of values for list of annotations lst
    lst is a list of the form [(start_time, stop_time, label)]
    dct is a dict in the form {label:corresponding numeric value}
    
    """
    if dct is None:
        levels = set(list(zip(*lst))[2])
        levels_num = [i for i in range(len(levels))]
        dct = { k:v for k,v in zip(levels, levels_num)}
    if return_levels_only:
        return [dct[lab] for _,_,lab in list(zip(*lst))]
    else:
        return [(stt, stp, dct[lab]) for stt, stp, lab in list(zip(*lst))]


#not working
# def get_intersection(lstA, lstB):
#     """ get intersection of two annotation lists"""
#     indA = 0
#     indB = 0
#     keepA = []
#     keepB = []
#     while indA<len(lstA) and indB<len(lstB):
#         #until B catches up with A
#         while indB<len(lstB) and lstB[indB][1]<=lstA[indA][0]:
#             indB+=1
#             if indB>=len(lstB):
#                 return keepA, keepB
#         #untill A catches up with B
#         while indA<len(lstA) and lstB[indB][0]>=lstA[indA][1]:
#             indA+=1
#             if indA>=len(lstA):
#                 return keepA, keepB
#         #intersection and maybe A covers B
#         if (lstA[indA][0]>lstB[indB][1]>lstA[indA][1]) or (lstA[indA][0]>lstB[indB][0]>lstA[indA][1]):
#             #check next B incase A overlapping several Bs
#             while indB<len(lstB) and lstB[indB][0]>lstA[indA][1]:#while B still in A
#                 keepB.append(indB)
#                 indB+=1
#             keepA.append(indA)
#             indA+=1
#         #B covers A
#         elif (lstB[indB][0]<lstA[indA][0]) and (lstB[indB][1]>lstA[indA][1]):
#             while indA<len(lstA) and lstA[indA][0]<lstB[indB][1]:
#                 keepA.append(indA)
#                 indA+=1
#             keepB.append(indB)
#             indB+=1
#     return keepA, keepB

def get_overlapping_segments(lstA, lstB):
    """get segments in A and B that overlap.
    
    Note: example lstA Roles lstB S&L
    
    Args:
        lstA (list of typles): [(start time, stop time, lab),..].
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
        elif (lstB[indB][0]<lstA[indA][0]) and (lstB[indB][1]>lstA[indA][1]):
            while indA<len(lstA) and lstA[indA][1]<lstB[indB][1]:
                if indA in dct:
                    dct[indA].append(indB)
                else:
                    dct[indA] = [indB]
                indA+=1
            indB+=1
    return dct

            