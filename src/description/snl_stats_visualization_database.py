import os, sys

script_path=os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")

from src.snl_stats_extraction_data import *
from IBPY.extract_data import *
from IBPY.visualization import *
DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers=get_parameters()


def display_general_informations_files(database):
    """ This function shows the general informations of the files.
    
    Args:
        database (list): list of all files paths
    Returns:
        list: list of tuples with the name of the file, the duration of the file and the number of tiers
    """
    real_tier_lists , real_tiers = get_parameters_tag()

    lst=[]
    lst_time=get_time_eaf(database)
    lst_count=get_tier_count(database, real_tier_lists.keys())
    for i in range(len(database)):
        file_info=os.path.split(database[i])[-1], lst_time[i], *lst_count[i][:len(real_tier_lists.keys())]
        lst.append(file_info)
    return lst

def display_specific_informations(database, tier, intensities, kind):
    """ This function shows the specific informations of the files filtered by a specific tier and entity.
    
    Args:
        database (list): list of all files paths
        tier (str): tier we search
        intensities (list): list of entities we search
    Returns:
        list: list of tuples with the name of the file, the duration of the file, the min time of the tier, the max time of the tier and the number of entities
    """
    lst=[]
    lst_tier_count=get_tier_intensities(database, tier, intensities, kind)
    lst_min_time, lst_max_time=get_max_min_time_tier(database, tier)
    temp=[]
    for i in range(len(database)):
        for intensity in intensities:
            temp.append(lst_tier_count[i][intensity])
        file_info=os.path.split(database[i])[-1], lst_min_time[i], lst_max_time[i], *temp[:len(temp)]
        lst.append(file_info)
        temp.clear()
    return lst