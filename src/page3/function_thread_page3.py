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
DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()

def create_intra_absolute_plot(database, queue, database_single, expression_choice):

    dg = get_db_from_func_no_pair(DIR, get_intra_tiers_absolute_duration_folder, database, expression_choice)      
    # print(dg[dg.database.eq(f'{database_single}')])
    scatter_fig_tiers=px.scatter(dg[dg.database.eq(f'{database_single.lower()}')], x='subject', y='sum_time', color='label'#,text='time'
    , orientation='v', title=f'{expression_choice} Absolute Duration - Intra , Database : ' + database_single, labels={"sum_time":"Absolute Duration",
    "label":"Entity"})
    line_fig_tiers=px.line(dg[dg.database.eq(f'{database_single.lower()}')], x='subject', y='sum_time', color='label', symbol='label',
    orientation='v', title=f'{expression_choice} Absolute Duration - Intra , Database : ' + database_single, labels={"sum_time":"Absolute Duration",
    "label":"Entity"})

    L= [scatter_fig_tiers, line_fig_tiers]

    queue.put(L)


def create_intra_relative_plot(database, queue, database_single, expression_choice) :

    dg = get_db_from_func_no_pair(DIR, get_intra_tiers_relative_duration_folder, database, expression_choice)

    scatter_fig_tiers=px.scatter(dg[dg.database.eq(f'{database_single.lower()}')], x='subject', y='percentage', color='label',
    orientation='v', title=f'{expression_choice} Relative Duration - Intra , Database : ' + database_single, labels={"label":"Entity"})
    line_fig_tiers=px.line(dg[dg.database.eq(f'{database_single.lower()}')], x='subject', y='percentage', color='label', symbol='label',
    orientation='v', title=f'{expression_choice} Relative Duration - Intra , Database : ' + database_single, labels={"label":"Entity"})

    L= [scatter_fig_tiers, line_fig_tiers ]

    queue.put(L)

def create_inter_absolute_plot(database, queue, database_single, expression_choice) :
    
    dg = get_db_from_func_pair(DIR, get_inter_tier_absolute_duration_folder, database, expression_choice, tier_lists)
        
    print(dg)
    fig1=px.scatter(dg[dg.database.eq(f'{database_single.lower()}')], x='conv', y='duration', color='label'
    #,text='time'
    , orientation='v', title=f'{expression_choice} Absolute Duration per interaction',labels={"conv":"Interaction",
    "duration":"Time difference","label":"Entity"})
    fig1_1=px.scatter(dg[dg.database.eq(f'{database_single.lower()}')], x='conv', y='duration', color='label'
    #,text='time'
    , orientation='v', title=f'{expression_choice} Absolute Duration per interaction',labels={"conv":"Interaction",
    "duration":"Time difference","label":"Entity"},trendline='rolling',trendline_options=dict(window=2))

    L = [fig1, fig1_1]
    queue.put(L)

def create_inter_relative_plot(database, queue, database_single, expression_choice) :

    dg = get_db_from_func_pair(DIR, get_inter_tier_relative_duration_folder, database, expression_choice, tier_lists)

    fig1=px.scatter(dg[dg.database.eq(f'{database_single.lower()}')], x='conv', y='percentage', color='label'
    , orientation='v', title=f'{expression_choice} Relative Duration per interaction', labels={"conv":"Interaction",
    "percentage":"Percentage difference","label":"Entity"})
    fig1_1=px.scatter(dg[dg.database.eq(f'{database_single.lower()}')], x='conv', y='percentage', color='label'
    #,text='time'
    , orientation='v', title=f'{expression_choice} Relative Duration per interaction',labels={"conv":"Interaction",
    "percentage":"Percentage difference","label":"Entity"},trendline='rolling',trendline_options=dict(window=2))

    L = [fig1, fig1_1]
    queue.put(L)       
        
