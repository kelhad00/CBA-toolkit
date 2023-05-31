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

#Others_______________________________________________________________
def plot_expression_per_min(folder,expression, case=None):
    """This function shows the count of expression we have per minute for smiles or laughs.

    Args:
        folder (list) -> list of all files paths
        expression (str) -> tiers we search
        case (int, optional): Express if you want to look into conversations ; for that, you put 2. Defaults to None.

    Returns:
        Figure: Bar plot
    """
    a=expression_per_min(folder,expression,case)

    split_elements = []

    for i in range(len(folder)) :
        element = folder[i]
        split_elements.append(element.split('\\'))

    if case is None:
        fig = px.bar(x=[split_elements[i][-1] for i in range(len(split_elements))], y=a[0], title=f'Count of {expression} per minute in {get_database_name(folder)}', 
        labels={'x':'File', 'y':'Count'})
    else:
        fig = px.bar(x = [split_elements[j][-1] + ' + ' + split_elements[j+1][-1] if (j+1) < len(split_elements) else None for j in range(0, len(split_elements), 2)]
        , y=a[0], title=f'Count of {expression} per minute in {get_database_name(folder)}', 
        labels={'x':'Pairs files', 'y':'Count'})

    if (np.count_nonzero(fig.data[0]['y']) == 0):

        return None
    
    return fig

def plot_expression_per_min_I(folder, expression, intensity):
    """This function shows the count of expression we have per minute for smiles or laughs by intensity.

    Args:
        folder (list) -> list of all files paths
        expression (str) -> tiers we search
        intensity (str) -> This is the intensity we search. You can type : subtle, low, medium, high for smiles and same for laughs (without subtle) for example

    Returns:
        Figure: Bar plot
    """
    fig = None


    try :
        lst=expression_per_min_I(folder, expression, intensity)
        color_lst=['orange', 'gray', 'white', 'yellow', 'black', 'blue', 'red', 'green', 'purple']

        split_elements = []

        for i in range(len(folder)) :
            element = folder[i]
            split_elements.append(element.split('\\'))

        for i in range (len(tier_lists[expression])):
            if intensity==tier_lists[expression][i]:
                fig = px.bar(x=[split_elements[i][-1] for i in range(len(split_elements))], y=lst, color_discrete_sequence =[color_lst[i]]*len(lst) ,
                title=f'Count of {intensity} {expression} per minute in {get_database_name(folder)}', labels={'x':'File', 'y':'Count'})

    
    except :

        fig = None

    
    return fig
