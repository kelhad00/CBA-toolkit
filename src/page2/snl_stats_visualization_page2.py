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
from .function_thread_page2 import *
from multiprocessing import Queue


def plot_absolute_duration(expression, choice):
    """Arg: expression (str) -> smiles or laughs"""
    
    
    if expression == "laughs":
        dg=get_db_from_func_no_pair(DIR,eval("get_"+expression+"_dict_folder"))
        labels = ["low", "medium", "high"]
    if expression == "smiles":
        dg=get_db_from_func_no_pair(DIR,eval("get_"+expression+"_dict_folder"))
        labels = ["subtle", "low", "medium", "high"] 

    if expression != 'both' :
        dg=get_db_from_func_no_pair(DIR,eval("get_"+expression+"_dict_folder"))
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
        fig.update_layout(title_text=f'Mean, median and standard deviation on laughs - Absolute Duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Time (ms)",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels,
            categoryorder='array',
            tickmode='array',
            tickvals=labels,
            ticktext=labels
        ))
        
        return fig
    
    else :
        #TODO: Changer Emotions par tiers
        Emotions = ['laughs', 'smiles']
        Threads = []
        D = []
        queue = Queue()
        for i in range(len(Emotions)) :
            
            Threads.append(threading.Thread(target=create_plot_absolute_duration_thread, args=(Emotions[i], choice,queue,)))

        for thread in Threads :

            thread.start()

        for thread in Threads :

            thread.join()
            D.append(queue.get())

        return D


def plot_relative_duration(expression):
    """Arg: expression (str) -> smiles or laughs"""
   

    if expression == "laughs":
        df=get_db_from_func_no_pair(DIR,eval("get_"+expression+"_dict_folder"))
        dg=get_rd_stats(df)
        dg=list_to_df(dg[0], dg[1])
        labels = ["low", "medium", "high"]
    if expression == "smiles":
        df=get_db_from_func_no_pair(DIR,eval("get_"+expression+"_dict_folder"))
        dg=get_rd_stats(df)
        dg=list_to_df(dg[0], dg[1])
        labels = ["subtle", "low", "medium", "high"]
    
    if expression != 'both' : 

        fig = make_subplots(rows=1, cols=3, subplot_titles=['Standard deviation', 'Mean', 'Median'])
        for database in (dg['database'].unique()):
            df_plot=dg[dg['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels)]
            
            fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database), row=1, col=1)
            fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database), row=1, col=2)
            fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database), row=1, col=3)
        fig.update_xaxes(categoryorder='array', categoryarray=labels, row=1, col=2)
        fig.update_xaxes(categoryorder='array', categoryarray=labels, row=1, col=3)
        fig.update_layout(boxmode='group', xaxis_tickangle=0)
        fig.update_layout(title_text=f'Mean, median and standard deviation on {expression} - Relative Duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Percentage",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels,
            categoryorder='array',
            tickmode='array',
            tickvals=labels,
            ticktext=labels,
        ))
        
        return fig
    
    else :

        Emotions = ['laughs', 'smiles']
        Threads = []
        D = []
        queue = Queue()
        for i in range(len(Emotions)) :
            Threads.append(threading.Thread(target=create_plot_relative_duration_thread, args=(Emotions[i],queue,)))
          
        for thread in Threads:

            thread.start()

        for thread in Threads : 

            thread.join()
            D.append(queue.get())
        return D  


#Filter by role
def plot_absolute_duration_from_spk(expression, choice):
    

    if expression == "laughs":
        labels = ["low", "medium", "high"]
    if expression == "smiles":
        labels = ["subtle", "low", "medium", "high"] 

    if expression != 'both' :

        dg=get_db_from_func_no_pair(DIR,eval("get_"+expression+"_from_spk_folder"))
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
        fig.update_layout(title_text=f'Mean, median and standard deviation for speaker {expression} absolute duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Time (ms)",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels,
            categoryorder='array',
            tickmode='array',
            tickvals=labels,
            ticktext=labels
        ))
        return fig
    
    else : 

        Threads = []
        D = []
        Emotions = ['laughs','smiles']
        queue = Queue()

        for i in range(len(Emotions)) : 
            print(Emotions[i])
            Threads.append(threading.Thread(target=create_absolute_duration_from_spk_thread, args=(Emotions[i], choice,queue,)))

        for thread in Threads : 

            thread.start()

        for thread in Threads :

            thread.join()
            D.append(queue.get())

        return D

def plot_relative_duration_from_spk(expression):

    if expression == "laughs":
        labels = ["low", "medium", "high"]
    if expression == "smiles":
        labels = ["subtle", "low", "medium", "high"] 

    if expression != 'both' : 

        df=get_db_from_func_no_pair(DIR,eval("get_"+expression+"_from_spk_folder"))
        dg=get_rd_stats_byrole(df)
        dg=list_to_df(dg[0], dg[1])
        fig = make_subplots(rows=1, cols=3, subplot_titles=['Standard deviation', 'Mean', 'Median'])
        for database in (dg['database'].unique()):
            df_plot=dg[dg['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels)]
            fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database), row=1, col=1)
            fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database), row=1, col=2)
            fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database), row=1, col=3)
        fig.update_xaxes(categoryorder='array', categoryarray=labels, row=1, col=2)
        fig.update_xaxes(categoryorder='array', categoryarray=labels, row=1, col=3)
        fig.update_layout(boxmode='group', xaxis_tickangle=0)
        fig.update_layout(title_text=f'Mean, median and standard deviation for speakers {expression} relative duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Percentage",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels,
            categoryorder='array',
            tickmode='array',
            tickvals=labels,
            ticktext=labels
        ))
        return fig

    else :

        Emotions = ['laughs', 'smiles']
        Threads = []
        D = []
        queue = Queue()

        for i in range(len(Emotions)):

            Threads.append(threading.Thread(target=create_relative_duration_from_spk_thread, args=(Emotions[i],queue,)))
        
        for thread in Threads :

            thread.start()    
        
        for thread in Threads:
            thread.join()
            D.append(queue.get())

        return D
    

def plot_absolute_duration_from_lsn(expression, choice):
    

    if expression == "laughs":
        labels = ["low", "medium", "high"]
    if expression == "smiles":
        labels = ["subtle", "low", "medium", "high"] 

    if expression != 'both' :
        dg=get_db_from_func_no_pair(DIR,eval("get_"+expression+"_from_lsn_folder"))
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
        fig.update_layout(title_text=f'Mean, median and standard deviation for listners {expression} absolute duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Time (ms)",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels,
            categoryorder='array',
            tickmode='array',
            tickvals=labels,
            ticktext=labels
        ))

        return fig
    
    else :

        Threads = []
        D= []
        Emotion = ['laughs', 'smiles']
        queue = Queue()

        for i in range(len(Emotions)):
            Threads.append(threading.Thread(target=create_absolute_duration_from_lsn_thread, args=(Emotion[i], choice,queue,)))

        for thread in Threads :

            thread.start()

        for thread in Threads :

            thread.join()
            D.append(queue.get())

        return D
    

def plot_relative_duration_from_lsn(expression):

   
    if expression == "laughs":
        labels = ["low", "medium", "high"]
    if expression == "smiles":
        labels = ["subtle", "low", "medium", "high"] 

    if expression != 'both' :

        df=get_db_from_func_no_pair(DIR,eval("get_"+expression+"_from_lsn_folder"))
        dg=get_rd_stats_byrole(df)
        dg=list_to_df(dg[0], dg[1])

        fig = make_subplots(rows=1, cols=3, subplot_titles=['Standard deviation', 'Mean', 'Median'])
        for database in (dg['database'].unique()):
            df_plot=dg[dg['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels)]
            fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database), row=1, col=1)
            fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database), row=1, col=2)
            fig.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database), row=1, col=3)
        fig.update_xaxes(categoryorder='array', categoryarray=labels, row=1, col=2)
        fig.update_xaxes(categoryorder='array', categoryarray=labels, row=1, col=3)
        fig.update_layout(boxmode='group', xaxis_tickangle=0)
        fig.update_layout(title_text=f'Mean, median and standard deviation for listeners {expression} relative duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Percentage",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels,
            categoryorder='array',
            tickmode='array',
            tickvals=labels,
            ticktext=labels
        ))
        return fig

    else :

        Emotion = ['laughs', 'smiles']
        Threads = []
        D = []
        queue = Queue()

        for i in range(len(Emotions)) :
            Threads.append(threading.Thread(target=create_relative_duration_from_lsn_thread, args=(Emotion[i],queue,)))
        
        for thread in Threads:
            thread.start()

        for thread in Threads:
            thread.join()
            D.append(queue.get())

        return D