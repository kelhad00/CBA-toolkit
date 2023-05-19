import os, sys, json
script_path = os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")
import time
result_thread = ""
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
    match = re.search(r'^([a-zA-Z]+)', expression)
    expression = match.group(1)
    if case is None:
        fig = px.bar(x=[_ for _ in range (1,len(a[0])+1)], y=a[0], title=f'Count of {expression[:6]} per minute in {get_database_name(folder)}', 
        labels={'x':'Person', 'y':'Count'})
    else:
        fig = px.bar(x=[_ for _ in range (1,len(a[0])+1)], y=a[0], title=f'Count of {expression[:6]} per minute in {get_database_name(folder)}', 
        labels={'x':'Interactions', 'y':'Count'})

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
    lst=expression_per_min_I(folder, expression, intensity)
    
    color_lst=["blue",'red','green','purple']
    
    for i in range (len(tier_lists[expression])):
        if intensity==tier_lists[expression][i]:
            fig = px.bar(x=[_ for _ in range (1,len(lst)+1)], y=lst, color_discrete_sequence =[color_lst[i]]*len(lst) ,
            title=f'Count of {intensity} {expression[:6]} per minute in {get_database_name(folder)}', labels={'x':'Person', 'y':'Count'})
    return fig

