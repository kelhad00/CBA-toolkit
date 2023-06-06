import os, sys

script_path=os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")

result_thread=""
import plotly.express as px
import plotly.graph_objects as pg
from plotly.subplots import make_subplots
from src.snl_stats_extraction_data import *
from IBPY.extract_data import *
from IBPY.visualization import *
import numpy as np
DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers=get_parameters()

#Until #Mimicry, all the functions below are plotting exactly what its written just after "plot_" in their names.

#Expression track - Intra __________________________________________________
def plot_track_previous_expression(dg, track_choice):
    """ Plot the previous expression track.
    
    Args:
        dg (dataframe): dataframe come from expression_track function
        track_choice (str): track choice
    Returns:
        fig: plot
    """
    if not dg.empty:
        fig=px.bar(dg, x='Trackp', y=['Countp'], color='Databasep', barmode='group',
        text=dg['Percentagep'].apply(lambda x: '{0:1.2f}%'.format(x))+dg['Countp'].apply(lambda x:'  /  [Count = {0} ]'.format(x)),
        labels={"Trackp": f"Previous {track_choice}", "Countp": f"Count Of Previous {track_choice}"},
                    title=f"Tracking Previous {track_choice.capitalize()}")
        fig.update_layout(yaxis_title=f"Count Of Previous {track_choice}")
    else:
        fig=None
    return fig

def plot_track_following_expression(dg, track_choice):
    """ Plot the following expression track.
    
    Args:
        dg (dataframe): dataframe come from expression_track function
        track_choice (str): track choice
    Returns:
        fig: plot
    """
    if not dg.empty:
        fig=px.bar(dg, x='Trackf', y=['Countf'], color='Databasef', barmode='group',
        text=dg['Percentagef'].apply(lambda x: '{0:1.2f}%'.format(x))+dg['Countf'].apply(lambda x:'  /  [Count = {0} ]'.format(x)),
        labels={"Trackf": f"Next {track_choice}", "Countf": f"Count Of Next {track_choice}"},
                    title=f"Tracking Next {track_choice.capitalize()}")
        fig.update_layout(yaxis_title=f"Count Of Next {track_choice}")
    else:
        fig=None
    return fig

#By Entity
def plot_track_previous_expression_byI(dg, track_choice, check_choice):
    """ Plot the previous expression track by entity.
    Args : 
        dg (dataframe): dataframe come from expression_track_byI function
        track_choice (str): track choice
        check_choice (str): check choice
    Returns:
        fig: plot
    """
    if not dg.empty:
        fig=px.bar(dg, x='Databasep', y=['Countp'], color='Intensityp', barmode='group', 
        facet_col=dg.iloc[:,2].name,
        text=dg['Percentagep'].apply(lambda x: '{0:1.2f}%'.format(x))+dg['Countp'].apply(lambda x:'  /  [Count = {0} ]'.format(x)),
        labels={"Intensityp": f"Entity Of Previous {check_choice}", "Countp": f"Count Of Previous {track_choice}"},
                    title=f"Tracking Previous {track_choice}")
        fig.for_each_xaxis(lambda axis: axis.update(title=f"Previous {track_choice}"))
        fig.update_layout(yaxis_title=f"Count Of Previous {track_choice}")
    else: 
        fig=None
    return fig

def plot_track_following_expression_byI(dg, track_choice, check_choice):
    """ Plot the following expression track by entity.
    
    Args :
        dg (dataframe): dataframe come from expression_track_byI function
        track_choice (str): track choice
        check_choice (str): check choice
    Returns:
        fig: plot
    """
    if not dg.empty:    
        fig=px.bar(dg, x='Databasef', y=['Countf'], color='Intensityf', barmode='group', 
        facet_col=dg.iloc[:,2].name,
        text=dg['Percentagef'].apply(lambda x: '{0:1.2f}%'.format(x))+dg['Countf'].apply(lambda x:'  /  [Count = {0} ]'.format(x)),
        labels={"Intensityf": f"Entity Of Next {check_choice}", "Countf": f"Count Of Next {track_choice}"},
                    title=f"Tracking Next {track_choice}")
        fig.for_each_xaxis(lambda axis: axis.update(title=f"Next {track_choice}"))
        fig.update_layout(yaxis_title=f"Count Of Next {track_choice}")
    else:
        fig=None
    return fig

#Mimicry______________________________________________________________
def plot_mimicry(L):
    """ Plot probabilities and count mimicry per interaction.
    L come from give_mimicry, or give_mimicry_folder1 or give_mimicry_folder2 or give_mimicry_folder3.
    
    Args:
        L (list): List of tuple (count, probability, database)
    Return : 
        Scatter (with line) plot figure
    """
    name_databases=[key.replace('_paths','') for key in databases.keys()]
    databases_=[value for value in databases_pair_paths.values()]
    # print(L[0][2])
    for i in range(len(name_databases)):
        if L[0][2]==name_databases[i]:
            data_path=databases_[i]
    split_elements=[]
    Pair_files=[]
    for i in range(len(data_path)):
        element=data_path[i]
        split_elements.append(element.split('\\'))
    for i in range(0,len(split_elements), 2): 
        Pair_files.append(split_elements[i][-1]+' / '+split_elements[i+1][-1])
    M=[]
    df=list_to_df(L,['count', 'probability', 'database'])
    if not df.empty:
        df['interaction']=[i+1 for i in range(len(df['count']))]
        lst=list(np.unique(list(df.database)))
        colors=['royalblue', 'green', 'red', 'orange']  # Specify colors for each line
        for i in lst:
            M.append(df[df.database.eq(i)])
        fig=make_subplots(1, len(lst))
        for i, j in zip([i for i in range(1,len(lst)+1)], M):
            for k in range(len(j['interaction'])):
                j['interaction'][k]=Pair_files[(int(j['interaction'][k])-1)]
            fig.add_trace(pg.Scatter(x=j['interaction'], y=j.probability, marker_color=colors[0], name=f'Propbabilities {lst[i-1]}'),1,i)
            fig.add_trace(pg.Scatter(x=j['interaction'], y=j['count'], marker_color=colors[1], name=f'Count {lst[i-1]}'), 1,i) 
        fig.update_layout(title=f'Count and probabilities per interaction')
        fig.update_xaxes(title='Pairs files')
    else:
        fig=None
    return fig

#Correlation__________________________________________________________
def plot_correlation(L, folder):
    """ This function plots the correlation between two series.
    
    Args:
        L (list): The list containing the correlation for each pair of two series
        folder (list): The list containing the path of the files
    Returns:
        Figure : Scatter plot
    """
    split_elements=[]
    Pair_Files=[]
    for i in range(len(folder)):
        element=folder[i]
        split_elements.append(element.split('\\'))
    for i in range(0,len(split_elements), 2): 
        Pair_Files.append(split_elements[i][-1]+' / '+split_elements[i+1][-1])
    if L:  
        fig=make_subplots(1, 1)
        fig.add_trace(pg.Scatter(x=[Pair_Files[i] for i in range(len(Pair_Files))], y=L, marker_color='royalblue', name='Correlation'))
        fig.update_layout(title=f'Correlation per interaction')
        fig.update_xaxes(title='Interaction')
        fig.update_yaxes(title='Correlation')
    else:
        fig=None
    return fig
    