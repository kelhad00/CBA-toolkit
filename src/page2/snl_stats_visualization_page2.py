import os, sys, json
from fuzzywuzzy import fuzz
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
from .function_thread_page2 import *
from multiprocessing import Queue

DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()

def plot_absolute_duration(expression, choice, name_databases):
    """Arg: expression (str) -> tiers
            choice (str) -> mean, median, standard deviation, min, max
            name_databases (list) -> list of databases
            
        Return: fig (plotly.graph_objects.Figure) -> plot of the choice for the expression
    """

    if expression != 'all' :
        labels = tier_lists[expression]
        dg=get_db_from_func_no_pair(DIR, eval("get_tier_dict_folder"), name_databases, expression)
        if not dg.empty:
            fig=pg.Figure()
            for database in (dg['database'].unique()):
                df_plot=dg[dg['database']==database]
                df_plot = df_plot[df_plot['label'].isin(labels)]
            
                if choice == 'Mean':
                    df_mean = df_plot.groupby('label').mean().reset_index()
                    fig.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
                elif choice == 'Median' : 
                    df_median = df_plot.groupby('label').median().reset_index()
                    fig.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
                elif choice == 'Standard deviation' :
                    df_std = df_plot.groupby('label').std().reset_index()
                    fig.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Min' :
                    df_std = df_plot.groupby('label').min().reset_index()
                    fig.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Max' :
                    df_std = df_plot.groupby('label').max().reset_index()
                    fig.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                else :
                    fig.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                        notched=True, boxmean='sd',
                                        name='database=' + database))

            fig.update_layout(boxmode='group', xaxis_tickangle=0)
            fig.update_layout(title_text=f'{choice} on {expression} - Absolute Duration', title_x=0.5, 
            xaxis_title="Entity",
            yaxis_title="Time (ms)",
            legend_title="Datasets",
            xaxis=dict(
                categoryarray=labels,
                categoryorder='array',
                tickmode='array',
                tickvals=labels,
                ticktext=labels
            ))
        else :
            fig = None
        return fig
    
    else :
        Tiers = list(tier_lists.keys())
        Threads = []
        D = []
        queue = Queue()
        for i in range(len(Tiers)) :
            Threads.append(threading.Thread(target=create_plot_absolute_duration_thread, args=(Tiers[i], choice, queue, name_databases)))
        for thread in Threads :
            thread.start()
        for thread in Threads :
            thread.join()
            D.append(queue.get())
        return D


def plot_relative_duration(expression, choice, name_databases):
    """Arg: expression (str) -> tiers
            choice (str) -> mean, median, standard deviation, min, max
            name_databases (list) -> list of databases
            
        Return: fig (plotly.graph_objects.Figure) -> plot of the choice for the expression
    """
    
    if expression != 'all' : 
        df = get_db_from_func_no_pair(DIR, eval("get_tier_dict_folder"), name_databases, expression)
        if not df.empty :
            dg = get_rd_stats(df)
            dg = list_to_df(dg[0], dg[1])
            labels = tier_lists[expression]
            fig = pg.Figure()
            for database in (dg['database'].unique()):
                df_plot = dg[dg['database'] == database]
                df_plot = df_plot[df_plot['label'].isin(labels)]
                if choice == 'Mean':
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database))
                elif choice == 'Median' : 
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database))
                elif choice == 'Standard deviation' :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database))
                elif choice == 'Min' :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name=database))
                elif choice == 'Max' :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name=database))
                else :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name='Mean ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name='Median ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name='Standard deviation ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name='Min ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name='Max ' + database))

            fig.update_layout(boxmode='group', xaxis_tickangle=0)
            fig.update_layout(title_text=f'{choice} on {expression} - Relative Duration', title_x=0.5, 
            xaxis_title="Entity",
            yaxis_title="Percentage",
            legend_title="Datasets",
            xaxis=dict(
                categoryarray=labels,
                categoryorder='array',
                tickmode='array',
                tickvals=labels,
                ticktext=labels,
            ))
        else :
            fig = None
        return fig
    else :
        Tiers = list(tier_lists.keys())
        Threads = []
        D = []
        queue = Queue()
        for i in range(len(Tiers)) :
            Threads.append(threading.Thread(target=create_plot_relative_duration_thread, args=(Tiers[i], choice, queue, name_databases)))
        for thread in Threads: 
            thread.start()
        for thread in Threads: 
            thread.join()
            D.append(queue.get())
        return D  


#Filter by role
def plot_absolute_duration_from_spk(expression, choice, name_databases):
    """Arg: expression (str) -> tiers
            choice (str) -> mean, median, standard deviation, min, max
            name_databases (list) -> list of databases
            
        Return: fig (plotly.graph_objects.Figure) -> plot of the choice for the expression
    """ 

    if expression != 'all' :
        labels = tier_lists[expression]
        dg=get_db_from_func_no_pair(DIR,eval("get_tier_from_spk_folder"), name_databases, expression)
        if not dg.empty :
            fig=pg.Figure()
            for database in (dg['database'].unique()):
                df_plot=dg[dg['database']==database]
                df_plot = df_plot[df_plot['label'].isin(labels)]
                if choice == 'Mean':
                    df_mean = df_plot.groupby('label').mean().reset_index()
                    fig.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
                elif choice == 'Median' : 
                    df_median = df_plot.groupby('label').median().reset_index()
                    fig.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
                elif choice == 'Standard deviation' :
                    df_std = df_plot.groupby('label').std().reset_index()
                    fig.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Min' :
                    df_std = df_plot.groupby('label').min().reset_index()
                    fig.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Max' :
                    df_std = df_plot.groupby('label').max().reset_index()
                    fig.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                else :
                    fig.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                        notched=True, boxmean='sd',
                                        name='database=' + database))

            fig.update_layout(boxmode='group', xaxis_tickangle=0)
            fig.update_layout(title_text=f'{choice} for speakers on {expression} - Absolute duration', title_x=0.5, 
            xaxis_title="Entity",
            yaxis_title="Time (ms)",
            legend_title="Datasets",
            xaxis=dict(
                categoryarray=labels,
                categoryorder='array',
                tickmode='array',
                tickvals=labels,
                ticktext=labels
            ))
        else :
            fig = None
        return fig
    
    else : 
        Threads = []
        D = []
        role_tier_name = next((key for key in tier_lists.keys() if fuzz.ratio(key.lower(), "role") >= 80), None)
        Tiers = list(tier_lists.keys())
        Tiers.remove(role_tier_name)
        queue = Queue()
        for i in range(len(Tiers)) : 
            print(Tiers[i])
            Threads.append(threading.Thread(target=create_absolute_duration_from_spk_thread, args=(Tiers[i], choice, queue, name_databases)))
        for thread in Threads : 
            thread.start()
        for thread in Threads :
            thread.join()
            D.append(queue.get())

        return D

def plot_relative_duration_from_spk(expression, choice, name_databases):
    """Arg: expression (str) -> tiers
            choice (str) -> mean, median, standard deviation, min, max
            name_databases (list) -> list of databases
            
        Return: fig (plotly.graph_objects.Figure) -> plot of the choice for the expression
    """

    if expression != 'all' : 
        labels = tier_lists[expression]
        df=get_db_from_func_no_pair(DIR,eval("get_tier_from_spk_folder"), name_databases, expression)
        if not df.empty :
            dg=get_rd_stats_byrole(df)
            dg=list_to_df(dg[0], dg[1])
            fig = pg.Figure()
            for database in (dg['database'].unique()):
                df_plot = dg[dg['database'] == database]
                df_plot = df_plot[df_plot['label'].isin(labels)]
                if choice == 'Mean':
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database))
                elif choice == 'Median' : 
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database))
                elif choice == 'Standard deviation' :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database))
                elif choice == 'Min' :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name=database))
                elif choice == 'Max' :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name=database))
                else :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name='Mean ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name='Median ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name='Standard deviation ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name='Min ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name='Max ' + database))

            fig.update_layout(boxmode='group', xaxis_tickangle=0)
            fig.update_layout(title_text=f'{choice} for speakers on {expression} - Relative duration', title_x=0.5, 
            xaxis_title="Entity",
            yaxis_title="Percentage",
            legend_title="Datasets",
            xaxis=dict(
                categoryarray=labels,
                categoryorder='array',
                tickmode='array',
                tickvals=labels,
                ticktext=labels
            ))
        else :
            fig = None
        return fig

    else :
        role_tier_name = next((key for key in tier_lists.keys() if fuzz.ratio(key.lower(), "role") >= 80), None)
        Tiers = list(tier_lists.keys())
        Tiers.remove(role_tier_name)
        Threads = []
        D = []
        queue = Queue()
        for i in range(len(Tiers)):
            Threads.append(threading.Thread(target=create_relative_duration_from_spk_thread, args=(Tiers[i], choice, queue, name_databases)))
        for thread in Threads :
            thread.start()    
        for thread in Threads:
            thread.join()
            D.append(queue.get())
        return D
    

def plot_absolute_duration_from_lsn(expression, choice, name_databases):
    """Arg: expression (str) -> tiers
            choice (str) -> mean, median, standard deviation, min, max
            name_databases (list) -> list of databases
            
        Return: fig (plotly.graph_objects.Figure) -> plot of the choice for the expression
    """

    if expression != 'all' :
        labels = tier_lists[expression]
        dg=get_db_from_func_no_pair(DIR,eval("get_tier_from_lsn_folder"), name_databases, expression)
        if not dg.empty :
            fig=pg.Figure()
            for database in (dg['database'].unique()):
                df_plot=dg[dg['database']==database]
                df_plot = df_plot[df_plot['label'].isin(labels)]
                if choice == 'Mean':
                    df_mean = df_plot.groupby('label').mean().reset_index()
                    fig.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
                elif choice == 'Median' : 
                    df_median = df_plot.groupby('label').median().reset_index()
                    fig.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
                elif choice == 'Standard deviation' :
                    df_std = df_plot.groupby('label').std().reset_index()
                    fig.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Min' :
                    df_std = df_plot.groupby('label').min().reset_index()
                    fig.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Max' :
                    df_std = df_plot.groupby('label').max().reset_index()
                    fig.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                else :
                    fig.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                        notched=True, boxmean='sd',
                                        name='database=' + database))

            fig.update_layout(boxmode='group', xaxis_tickangle=0)
            fig.update_layout(title_text=f'{choice} for listeners on {expression} - Absolute duration', title_x=0.5, 
            xaxis_title="Entity",
            yaxis_title="Time (ms)",
            legend_title="Datasets",
            xaxis=dict(
                categoryarray=labels,
                categoryorder='array',
                tickmode='array',
                tickvals=labels,
                ticktext=labels
            ))
        else :
            fig = None
        return fig
    
    else :
        Threads = []
        D= []
        role_tier_name = next((key for key in tier_lists.keys() if fuzz.ratio(key.lower(), "role") >= 80), None)
        Tiers = list(tier_lists.keys())
        Tiers.remove(role_tier_name)
        queue = Queue()
        for i in range(len(Tiers)):
            Threads.append(threading.Thread(target=create_absolute_duration_from_lsn_thread, args=(Tiers[i], choice, queue, name_databases)))
        for thread in Threads :
            thread.start()
        for thread in Threads :
            thread.join()
            D.append(queue.get())

        return D
    

def plot_relative_duration_from_lsn(expression, choice, name_databases):
    """Arg: expression (str) -> tiers
            choice (str) -> mean, median, standard deviation, min, max
            name_databases (list) -> list of databases
            
        Return: fig (plotly.graph_objects.Figure) -> plot of the choice for the expression
    """

    if expression != 'all' :
        labels = tier_lists[expression]
        df=get_db_from_func_no_pair(DIR,eval("get_tier_from_lsn_folder"), name_databases, expression)
        if not df.empty :
            dg=get_rd_stats_byrole(df)
            dg=list_to_df(dg[0], dg[1])
            fig = pg.Figure()
            for database in (dg['database'].unique()):
                df_plot = dg[dg['database'] == database]
                df_plot = df_plot[df_plot['label'].isin(labels)]
                if choice == 'Mean':
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database))
                elif choice == 'Median' : 
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database))
                elif choice == 'Standard deviation' :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database))
                elif choice == 'Min' :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name=database))
                elif choice == 'Max' :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name=database))
                else :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name='Mean ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name='Median ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name='Standard deviation ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name='Min ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name='Max ' + database))

            fig.update_layout(boxmode='group', xaxis_tickangle=0)
            fig.update_layout(title_text=f'{choice} for listeners on {expression} - Relative duration', title_x=0.5, 
            xaxis_title="Entity",
            yaxis_title="Percentage",
            legend_title="Datasets",
            xaxis=dict(
                categoryarray=labels,
                categoryorder='array',
                tickmode='array',
                tickvals=labels,
                ticktext=labels
            ))
        else :
            fig = None
        return fig

    else :
        role_tier_name = next((key for key in tier_lists.keys() if fuzz.ratio(key.lower(), "role") >= 80), None)
        Tiers = list(tier_lists.keys())
        Tiers.remove(role_tier_name)
        Threads = []
        D = []
        queue = Queue()
        for i in range(len(Tiers)) :
            Threads.append(threading.Thread(target=create_relative_duration_from_lsn_thread, args=(Tiers[i], choice, queue, name_databases)))
        for thread in Threads:
            thread.start()
        for thread in Threads:
            thread.join()
            D.append(queue.get())

        return D

#Filter by tier
def plot_absolute_duration_from_tier(tier1, entity, tier2, choice, name_databases):
    """Arg: tier1 (str) -> tier of the entity to retrieve the other tier
            entity (str) -> entity or Entity of tier1
            tier2 (str) -> tier to retrieve
            choice (str) -> mean, median, standard deviation, min, max
            name_databases (list) -> list of databases
            
        Return: fig (plotly.graph_objects.Figure) -> plot of the choice for the expression
    """
    if tier2 != 'all' :
        labels = tier_lists[tier2]
        dg=get_db_from_func_no_pair_tier(DIR,eval("get_tier_from_tier"), name_databases, tier1, tier2, entity)
        if not dg.empty :
            fig=pg.Figure()
            for database in (dg['database'].unique()):
                df_plot=dg[dg['database']==database]
                df_plot = df_plot[df_plot['label'].isin(labels)]
                if choice == 'Mean':
                    df_mean = df_plot.groupby('label').mean().reset_index()
                    fig.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
                elif choice == 'Median' : 
                    df_median = df_plot.groupby('label').median().reset_index()
                    fig.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
                elif choice == 'Standard deviation' :
                    df_std = df_plot.groupby('label').std().reset_index()
                    fig.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Min' :
                    df_std = df_plot.groupby('label').min().reset_index()
                    fig.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Max' :
                    df_std = df_plot.groupby('label').max().reset_index()
                    fig.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                else :
                    fig.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                        notched=True, boxmean='sd',
                                        name='database=' + database))

            fig.update_layout(boxmode='group', xaxis_tickangle=0)
            fig.update_layout(title_text=f'{choice} for {entity} {tier1} on {tier2} - Absolute duration', title_x=0.5, 
            xaxis_title="Entity",
            yaxis_title="Time (ms)",
            legend_title="Datasets",
            xaxis=dict(
                categoryarray=labels,
                categoryorder='array',
                tickmode='array',
                tickvals=labels,
                ticktext=labels
            ))
        else :
            fig = None
        return fig
    
    else :
        Threads = []
        D= []
        Tiers = list(tier_lists.keys())
        Tiers.remove(tier1)
        queue = Queue()
        for i in range(len(Tiers)):
            Threads.append(threading.Thread(target=create_absolute_duration_from_tier_thread, args=(Tiers[i], choice, queue, name_databases, tier1, entity)))
        for thread in Threads :
            thread.start()
        for thread in Threads :
            thread.join()
            D.append(queue.get())

        return D


def plot_relative_duration_from_tier(tier1, entity, tier2, choice, name_databases):
    """Arg: tier1 (str) -> tier of the entity to retrieve the other tier
            entity (str) -> entity or Entity of tier1
            tier2 (str) -> tier to retrieve
            choice (str) -> mean, median, standard deviation, min, max
            name_databases (list) -> list of databases
            
        Return: fig (plotly.graph_objects.Figure) -> plot of the choice for the expression
    """
    if tier2 != 'all' :
        labels = tier_lists[tier2]
        df=get_db_from_func_no_pair_tier(DIR,eval("get_tier_from_tier"), name_databases, tier1, tier2, entity)
        print(df)
        if not df.empty :
            dg=get_rd_stats_byrole(df)
            dg=list_to_df(dg[0], dg[1])
            fig = pg.Figure()
            for database in (dg['database'].unique()):
                df_plot = dg[dg['database'] == database]
                df_plot = df_plot[df_plot['label'].isin(labels)]
                if choice == 'Mean':
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database))
                elif choice == 'Median' : 
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database))
                elif choice == 'Standard deviation' :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database))
                elif choice == 'Min' :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name=database))
                elif choice == 'Max' :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name=database))
                else :
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name='Mean ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name='Median ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name='Standard deviation ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name='Min ' + database))
                    fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name='Max ' + database))

            fig.update_layout(boxmode='group', xaxis_tickangle=0)
            fig.update_layout(title_text=f'{choice} for {entity} {tier1} on {tier2} - Relative duration', title_x=0.5, 
            xaxis_title="Entity",
            yaxis_title="Percentage",
            legend_title="Datasets",
            xaxis=dict(
                categoryarray=labels,
                categoryorder='array',
                tickmode='array',
                tickvals=labels,
                ticktext=labels
            ))
        else :
            fig = None
        return fig

    else :
        Tiers = list(tier_lists.keys())
        Tiers.remove(tier1)
        Threads = []
        D = []
        queue = Queue()
        for i in range(len(Tiers)) :
            Threads.append(threading.Thread(target=create_relative_duration_from_tier_thread, args=(Tiers[i], choice, queue, name_databases, tier1, entity)))
        for thread in Threads:
            thread.start()
        for thread in Threads:
            thread.join()
            D.append(queue.get())

        return D