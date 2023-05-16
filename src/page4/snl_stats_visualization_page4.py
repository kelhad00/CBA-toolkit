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

#Until #Mimicry, all the functions below are plotting exactly what its written just after "plot_" in their names.

#S&L track - Intra __________________________________________________
def plot_track_previous_SL(dg, track_choice):
    """Args : The dataframe come from SL_track function"""

    if track_choice == 'S':
        track_choice = 'Smiles'
    elif track_choice == 'L':
        track_choice = 'Laughs'

    fig=px.bar(dg, x='Trackp', y=['Countp'], color='Databasep', barmode='group',
    text=dg['Percentagep'].apply(lambda x: '{0:1.2f}%'.format(x)) + dg['Countp'].apply(lambda x:'  /  [Count = {0} ]'.format(x)),
    labels={"Trackp": f"Previous {track_choice}"},
                title=f"Tracking Previous {track_choice.capitalize()}")
    #fig.show()
    return fig
def plot_track_following_SL(dg, track_choice):
    """Args : The dataframe come from SL_track function"""

    if track_choice == 'S':
        track_choice = 'Smiles'
    elif track_choice == 'L':
        track_choice = 'Laughs'

    fig=px.bar(dg, x='Trackf', y=['Countf'], color='Databasef', barmode='group',
    text=dg['Percentagef'].apply(lambda x: '{0:1.2f}%'.format(x)) + dg['Countf'].apply(lambda x:'  /  [Count = {0} ]'.format(x)),
    labels={"Trackf": f"Next {track_choice}"},
                title=f"Tracking Next {track_choice.capitalize()}")
    #fig.show()
    return fig

#By intensity
def plot_track_previous_SL_byI(dg, track_choice):
    """Args : The dataframe comes from SL_track_byI function"""
    
    if track_choice == 'S':
        track_choice = 'Smiles'
    elif track_choice == 'L':
        track_choice = 'Laughs'

    fig=px.bar(dg, x='Databasep', y=['Countp'], color='Intensityp', barmode='group', 
    facet_col=dg.iloc[:,2].name,
    text=dg['Percentagep'].apply(lambda x: '{0:1.2f}%'.format(x)) + dg['Countp'].apply(lambda x:'  /  [Count = {0} ]'.format(x)),
    labels={"Intensityp": f"Intensity Of Previous {track_choice}"},
                title=f"Tracking Previous {track_choice}")
    fig.for_each_xaxis(lambda axis: axis.update(title=f"Previous {track_choice}"))
    #fig.show()
    return fig

def plot_track_following_SL_byI(dg, track_choice):
    """Args : The dataframe come from SL_track_byI function"""
    
    fig=px.bar(dg, x='Databasef', y=['Countf'], color='Intensityf', barmode='group', 
    facet_col=dg.iloc[:,2].name,
    text=dg['Percentagef'].apply(lambda x: '{0:1.2f}%'.format(x)) + dg['Countf'].apply(lambda x:'  /  [Count = {0} ]'.format(x)),
    labels={"Intensityf": f"Intensity Of Next {track_choice}"},
                title=f"Tracking Next {track_choice}")
    fig.for_each_xaxis(lambda axis: axis.update(title=f"Next {track_choice}"))
    #fig1.show()
    return fig

    #Mimicry______________________________________________________________
def plot_mimicry(L):
    """Plot probabilities and count mimicry per interaction.
    L come from give_mimicry, or give_mimicry_folder1 or give_mimicry_folder2
    Args:
        L (list): List of tuple (count, probability, database)
    Return : 
        Scatter (with line) plot figure
    """
    M=[]
    df=list_to_df(L,['count','probability','database'])
    df['interaction']=[i+1 for i in range(len(df['count']))]
    
    lst=list(np.unique(list(df.database)))
    for i in lst:
        M.append(df[df.database.eq(i)])
    fig = make_subplots(1, len(lst))
    for i,j in zip ([i for i in range(1,len(lst)+1)],M):
        fig.add_trace(pg.Scatter(x=j['interaction'], y=j.probability, marker_color = 'royalblue', name=f'Propbabilities {lst[i-1]}'),1,i)
        fig.add_trace(pg.Scatter(x=j['interaction'], y=j['count'], name=f'Count {lst[i-1]}'), 1,i) 
    fig.update_layout(title=f'Count and probabilities per interaction ')
    fig.update_xaxes(title='Interaction')
    #fig.show()
    return fig

#Correlation__________________________________________________________
def plot_correlation(L):
    """This function plots the correlation between two series.

    Args:
        L (list): The list containing the correlation for each pair of two series.

    Returns:
        Figure : Scatter plot
    """
    
    fig = make_subplots(1, 1)
    fig.add_trace(pg.Scatter(y=L, marker_color = 'royalblue', name='Correlation'))
    fig.update_layout(title=f'Correlation per interaction ')
    fig.update_xaxes(title='Interaction')
    fig.update_yaxes(title='Correlation')
    #fig.show()
    return fig
    