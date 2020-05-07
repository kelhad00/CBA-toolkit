def tuple_to_sequence(lst, width, shift):
    """Convert [(strt, stp, val)] to sequence of val.
    
    Args:
        lst (list): start and stop times of each val.
        width (numeric): window width in ms.
        shift (numeric): window shift in ms.
    
    Returns:
        list: sequence of vals corresponding to the tuples in lst.
    """
    lst = sorted(lst)
    seq = []
    last_frame = (lst[-1][1] - width) / shift
    frame_id = 0
    ind = 0
    while (frame_id * shift) < last_frame and ind < len(lst):
        if lst[ind][1] >= (frame_id * shift) >= lst[ind][0]:
            while (frame_id * shift) <= lst[ind][1]:
                seq.append(lst[ind][2])
                frame_id += 1
            ind += 1
        else:
            while (frame_id * shift) < lst[ind][0]:
                seq.append(None)
                frame_id += 1
                if (frame_id * shift) >= last_frame:
                    return seq
    return seq
