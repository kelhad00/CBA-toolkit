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
        return [dct[lab] for _,_,lab in lst]
    else:
        return [(stt, stp, dct[lab]) for stt, stp, lab in lst]


def tuple_to_sequence(lst, width, shift):
    """convert list of tuples (start time, stop time, label) to sequence of labels.
    With and shift should be in ms."""

    lst = sorted(lst)
    seq = []
    last_frame = (lst[-1][1]-width)/shift
    frame_id = 0
    ind = 0
    while (frame_id*shift)<last_frame and ind<len(lst):
        if lst[ind][1]>=(frame_id*shift)>=lst[ind][0]:
            while (frame_id*shift)<=lst[ind][1]:
                seq.append(lst[ind][2])
                frame_id+=1
            ind+=1
        else:
            while (frame_id*shift)<lst[ind][0]:
                seq.append(None)
                frame_id+=1
                if (frame_id*shift)>=last_frame:
                    return seq
    return seq