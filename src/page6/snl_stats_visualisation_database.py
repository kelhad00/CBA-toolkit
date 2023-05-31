import os, sys, json
script_path = os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")
import time
import matplotlib.pyplot as plt
import seaborn as sn
import plotly.express as px
import plotly.graph_objects as pg
from plotly.subplots import make_subplots
from src.snl_stats_extraction_data import *
from IBPY.extract_data import *
from IBPY.visualization import *
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import threading

DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()

def display_general_informations_files(database):

    lst = []
    lst_time = get_time_eaf(database)
    lst_count = get_tier_count(database,tier_lists.keys())

    for i in range(len(database)) :

        file_info = database[i].split('\\')[-1], lst_time[i], *lst_count[i][:len(tier_lists.keys())]
        lst.append(file_info)

    return lst

def display_specific_informations(database, tier, intensities) :
    lst = []
    lst_tier_count = get_tier_intensities(database, tier, intensities)
    lst_min_time, lst_max_time = get_max_min_time_tier(database, tier)
    temp = []
    for i in range(len(database)) :
        for intensity in intensities :
            temp.append(lst_tier_count[i][intensity])
        file_info = database[i].split('\\')[-1], lst_min_time[i], lst_max_time[i], *temp[:len(temp)]
        lst.append(file_info)
        temp.clear()
        
    return lst