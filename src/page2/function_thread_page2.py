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
def create_plot_absolute_duration_thread(Tiers, choice, queue, name_databases) :

    dg1 = get_db_from_func_no_pair(DIR, eval("get_tier_dict_folder"), name_databases, Tiers)
    fig1=pg.Figure()
    if not dg1.empty :
        labels1 = tier_lists[Tiers]   

        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels1)]
            if not df_plot.empty :
                if choice == 'Mean':
                    df_mean = df_plot.groupby('label').mean().reset_index()
                    fig1.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
                elif choice == 'Median' : 
                    df_median = df_plot.groupby('label').median().reset_index()
                    fig1.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
                elif choice == 'Standard deviation' :
                    df_std = df_plot.groupby('label').std().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Min' :
                    df_std = df_plot.groupby('label').min().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Max' :
                    df_std = df_plot.groupby('label').max().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                else :
                    fig1.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                        notched=True, boxmean='sd',
                                        name='database=' + database))

        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'{choice} on {Tiers} - Absolute Duration', title_x=0.5, 
        xaxis_title="Entity",
        yaxis_title="Time (ms)",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels1,
            categoryorder='array',
            tickmode='array',
            tickvals=labels1,
            ticktext=labels1
        ))
    else :
        fig1 = None

    queue.put(fig1)



def create_plot_relative_duration_thread(Tiers, choice, queue, database_names) :
        
    df1 = get_db_from_func_no_pair(DIR, eval("get_tier_dict_folder"), database_names, Tiers)
    if not df1.empty :
        dg1 = get_rd_stats(df1)
        dg1 = list_to_df(dg1[0], dg1[1])
        labels1 = tier_lists[Tiers]     
        
        fig1 = pg.Figure()
        for database in (dg1['database'].unique()):
            df_plot = dg1[dg1['database'] == database]
            df_plot = df_plot[df_plot['label'].isin(labels1)]
            if choice == 'Mean':
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database))
            elif choice == 'Median' : 
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database))
            elif choice == 'Standard deviation' :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database))
            elif choice == 'Min' :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name=database))
            elif choice == 'Max' :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name=database))
            else :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name='Mean ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name='Median ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name='Standard deviation ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name='Min ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name='Max ' + database))

        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'{choice} on {Tiers} - Relative Duration', title_x=0.5, 
        xaxis_title="Entity",
        yaxis_title="Percentage",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels1,
            categoryorder='array',
            tickmode='array',
            tickvals=labels1,
            ticktext=labels1,
        ))
    else :
        fig1 = None

    queue.put(fig1)
    
#Filter by role   
def create_absolute_duration_from_spk_thread(Tiers, choice, queue, name_databases) :

    labels = tier_lists[Tiers]
    dg1=get_db_from_func_no_pair(DIR,eval("get_tier_from_spk_folder"), name_databases, Tiers)
    fig1=pg.Figure()
    if not dg1.empty :
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels)]
            if not df_plot.empty :
                if choice == 'Mean':
                    df_mean = df_plot.groupby('label').mean().reset_index()
                    fig1.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
                elif choice == 'Median' : 
                    df_median = df_plot.groupby('label').median().reset_index()
                    fig1.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
                elif choice == 'Standard deviation' :
                    df_std = df_plot.groupby('label').std().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Min' :
                    df_std = df_plot.groupby('label').min().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Max' :
                    df_std = df_plot.groupby('label').max().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                else :
                    fig1.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                        notched=True, boxmean='sd',
                                        name='database=' + database))

        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'{choice} for speakers on {Tiers} - Absolute duration', title_x=0.5, 
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
        fig1 = None

    queue.put(fig1)


def create_relative_duration_from_spk_thread(Tiers, choice, queue, name_databases) :

    labels = tier_lists[Tiers] 

    df1=get_db_from_func_no_pair(DIR,eval("get_tier_from_spk_folder"), name_databases, Tiers)
    if not df1.empty :
        dg1=get_rd_stats_byrole(df1)
        dg1=list_to_df(dg1[0], dg1[1])
        fig1 = pg.Figure()
        for database in (dg1['database'].unique()):
            df_plot = dg1[dg1['database'] == database]
            df_plot = df_plot[df_plot['label'].isin(labels)]
            if choice == 'Mean':
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database))
            elif choice == 'Median' : 
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database))
            elif choice == 'Standard deviation' :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database))
            elif choice == 'Min' :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name=database))
            elif choice == 'Max' :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name=database))
            else :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name='Mean ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name='Median ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name='Standard deviation ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name='Min ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name='Max ' + database))

        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'{choice} for speakers on {Tiers} - Relative duration', title_x=0.5, 
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
        fig1 = None

    queue.put(fig1)


  
def create_absolute_duration_from_lsn_thread(Tiers, choice, queue, name_databases) :

    labels = tier_lists[Tiers]

    dg1=get_db_from_func_no_pair(DIR,eval("get_tier_from_lsn_folder"), name_databases, Tiers)
    fig1=pg.Figure()
    if not dg1.empty :
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels)]
            if not df_plot.empty :
                if choice == 'Mean':
                    df_mean = df_plot.groupby('label').mean().reset_index()
                    fig1.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
                elif choice == 'Median' : 
                    df_median = df_plot.groupby('label').median().reset_index()
                    fig1.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
                elif choice == 'Standard deviation' :
                    df_std = df_plot.groupby('label').std().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Min' :
                    df_std = df_plot.groupby('label').min().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Max' :
                    df_std = df_plot.groupby('label').max().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                else :
                    fig1.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                        notched=True, boxmean='sd',
                                        name='database=' + database))

        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'{choice} for listeners on {Tiers} - Absolute duration', title_x=0.5, 
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
        fig1 = None

    queue.put(fig1)

    
def create_relative_duration_from_lsn_thread(Tiers, choice, queue, name_databases) :

    labels = tier_lists[Tiers]
    
    df1=get_db_from_func_no_pair(DIR,eval("get_tier_from_lsn_folder"), name_databases, Tiers)
    if not df1.empty :
        dg1=get_rd_stats_byrole(df1)
        dg1=list_to_df(dg1[0], dg1[1])

        fig1 = pg.Figure()
        for database in (dg1['database'].unique()):
            df_plot = dg1[dg1['database'] == database]
            df_plot = df_plot[df_plot['label'].isin(labels)]
            if choice == 'Mean':
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database))
            elif choice == 'Median' : 
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database))
            elif choice == 'Standard deviation' :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database))
            elif choice == 'Min' :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name=database))
            elif choice == 'Max' :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name=database))
            else :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name='Mean ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name='Median ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name='Standard deviation ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name='Min ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name='Max ' + database))

        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'{choice} for listeners on {Tiers} - Relative duration', title_x=0.5, 
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
       fig1 = None

    queue.put(fig1)

#Filter by tier 
def create_absolute_duration_from_tier_thread(Tiers, choice, queue, name_databases, tier1, entity) :
    
    labels = tier_lists[Tiers]

    dg1=get_db_from_func_no_pair_tier(DIR,eval("get_tier_from_tier"), name_databases, tier1, Tiers, entity)
    fig1=pg.Figure()
    if not dg1.empty :
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels)]
            if not df_plot.empty :
                if choice == 'Mean':
                    df_mean = df_plot.groupby('label').mean().reset_index()
                    fig1.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
                elif choice == 'Median' : 
                    df_median = df_plot.groupby('label').median().reset_index()
                    fig1.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
                elif choice == 'Standard deviation' :
                    df_std = df_plot.groupby('label').std().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Min' :
                    df_std = df_plot.groupby('label').min().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice == 'Max' :
                    df_std = df_plot.groupby('label').max().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                else :
                    fig1.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                        notched=True, boxmean='sd',
                                        name='database=' + database))

        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'{choice} for {entity} {tier1} on {Tiers} - Absolute duration', title_x=0.5, 
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
        fig1 = None

    queue.put(fig1)

def create_relative_duration_from_tier_thread(Tiers, choice, queue, name_databases, tier1, entity) :
    labels = tier_lists[Tiers]
    
    df1 = get_db_from_func_no_pair_tier(DIR,eval("get_tier_from_tier"), name_databases, tier1, Tiers, entity)
    if not df1.empty :
        dg1=get_rd_stats_byrole(df1)
        dg1=list_to_df(dg1[0], dg1[1])

        fig1 = pg.Figure()
        for database in (dg1['database'].unique()):
            df_plot = dg1[dg1['database'] == database]
            df_plot = df_plot[df_plot['label'].isin(labels)]
            if choice == 'Mean':
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database))
            elif choice == 'Median' : 
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database))
            elif choice == 'Standard deviation' :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database))
            elif choice == 'Min' :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name=database))
            elif choice == 'Max' :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name=database))
            else :
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name='Mean ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name='Median ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name='Standard deviation ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name='Min ' + database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name='Max ' + database))

        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'{choice} for {entity} {tier1} on {Tiers} - Relative duration', title_x=0.5, 
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
        fig1 = None

    queue.put(fig1)