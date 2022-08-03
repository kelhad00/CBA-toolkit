import matplotlib.pyplot as plt


# def plot_overlapping_tiers_same_colors(dct, lstA, lstB):
#     """Visualize segments of 2 tiers in a gant graph.
#     Colors alternate between successive segments.
    
#     Args:
#         dct (dict): output of get_overlapping_segments_ind
#         lstA (list): [(strt, stp, val)]
#         lstB (list): [(strt, stp, val)]
#     """
#     _, ax = plt.subplots()
#     ypos = [1, 0.5]
#     id_col = -1
#     col = {-1: "blue", 1: "orange"}
#     for indA, B in dct.items():
#         widthA = lstA[indA][1] - lstA[indA][0]
#         leftA = lstA[indA][0]
#         for indB in B:#if overlap with 2 A segments consider it overlapping second one
#             widthB = lstB[indB][1] - lstB[indB][0]
#             leftB = lstB[indB][0]
#             ax.barh(
#                 y=ypos,
#                 width=[widthA, widthB],
#                 left=[leftA, leftB],
#                 height=0.1,
#                 color=col[id_col],
#             )
#         id_col *= -1
#     first = list(dct.keys())[0]
#     last = list(dct.keys())[-1]
#     ax.set_yticks(ypos)
#     ax.set_yticklabels(["A", "B"])
#     plt.xlim(
#         [lstA[first][0] - 0.1 * lstA[first][0], lstA[last][1] + 0.1 * lstA[last][1]]
#     )
#     return


def plot_overlapping_tiers_same_colors(dct):
    """Same as above but does not require lstA and lstB.

    Args:
        dct (dict): output of get_overlapping_segments
    """
    _, ax = plt.subplots()
    ypos = [1, 0.5]
    id_col = -1
    col = {-1: "blue", 1: "orange"}
    for segA, segB in dct.items():
        widthA = segA[1] - segA[0]
        leftA = segA[0]
        for ind in range(len(segB)):
            widthB = segB[ind][1] - segB[ind][0]
            leftB = segB[ind][0]
            ax.barh(
                y=ypos,
                width=[widthA, widthB],
                left=[leftA, leftB],
                height=0.1,
                color=col[id_col],
            )
        id_col *= -1
    first = list(dct.keys())[0]
    last = list(dct.keys())[-1]
    ax.set_yticks(ypos)
    ax.set_yticklabels(["A", "B"])
    plt.xlim(
        [
            first[0] - 0.1 * first[0],
            last[1] + 0.1 * last[1]
        ]
    )
    return


def plot_tiers(dct):
    """visualize segments of tiers in a gant graph.
    dct is a dict of {tier:[(strt, stp, val)]}"""
    _, ax = plt.subplots()
    y = 1
    ticks_pos = []
    ticks_names = []
    for name, lst in dct.items():
        if len(lst) == 0:
            continue
        for (strt, stp, _) in lst:
            width = stp - strt
            ax.barh(y, width=width, left=strt, height=0.1, color="blue")
        ticks_pos.append(y)
        ticks_names.append(name)
        y += 1
    ax.set_yticks(ticks_pos)
    ax.set_yticklabels(ticks_names)
    return
