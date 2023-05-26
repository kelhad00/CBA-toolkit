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

def create_inter_absolute_plot(database_single, queue) :

    dg = get_db_from_func_pair(DIR, get_inter_smiles_absolute_duration_folder)
        
    print(dg)
    fig1=px.scatter(dg[dg.database.eq(f'{database_single}')], x='conv', y='duration', color='label'
    #,text='time'
    , orientation='v', title='Smiles Absolute Duration per interaction',labels={"conv":"Interaction",
    "duration":"Time difference","label":"Intensity"})
    fig1_1=px.scatter(dg[dg.database.eq(f'{database_single}')], x='conv', y='duration', color='label'
    #,text='time'
    , orientation='v', title='Smiles Absolute Duration per interaction',labels={"conv":"Interaction",
    "duration":"Time difference","label":"Intensity"},trendline='rolling',trendline_options=dict(window=2))

    df = get_db_from_func_pair(DIR, get_inter_laughs_absolute_duration_folder)

    fig2=px.scatter(df[df.database.eq(f'{database_single}')], x='conv', y='duration', color='label'
    #,text='time'
    , orientation='v', title='Laughs Absolute Duration per interaction',labels={"conv":"Interaction",
    "duration":"Time difference","label":"Intensity"})
    fig2_2=px.scatter(df[df.database.eq(f'{database_single}')], x='conv', y='duration', color='label'
    #,text='time'
    , orientation='v', title='Laughs Absolute Duration per interaction',labels={"conv":"Interaction",
    "duration":"Time difference","label":"Intensity"},trendline='rolling',trendline_options=dict(window=2))
        
    # #fig1.show()
    # fig1_1.show()
    # #fig2.show()
    # fig2_2.show()
    L = [fig1, fig1_1, fig2, fig2_2]
    queue.put(L)

def create_inter_relative_plot(database_single, queue) :

    dg = get_db_from_func_pair(DIR, get_inter_smiles_relative_duration_folder)

    fig1=px.scatter(dg[dg.database.eq(f'{database_single}')], x='conv', y='percentage', color='label'
    , orientation='v', title='Smiles Relative Duration per interaction', labels={"conv":"Interaction",
    "percentage":"Percentage difference","label":"Intensity"})
    fig1_1=px.scatter(dg[dg.database.eq(f'{database_single}')], x='conv', y='percentage', color='label'
    #,text='time'
    , orientation='v', title='Smiles Relative Duration per interaction',labels={"conv":"Interaction",
    "percentage":"Percentage difference","label":"Intensity"},trendline='rolling',trendline_options=dict(window=2))

    df = get_db_from_func_pair(DIR, get_inter_laughs_relative_duration_folder)

    fig2=px.scatter(df[df.database.eq(f'{database_single}')], x='conv', y='percentage', color='label'
    , orientation='v', labels={"conv":"Interaction","percentage":"Percentage difference",
    "label":"Intensity"},title='Laughs Relative Duration per interaction')
    fig2_2=px.scatter(df[df.database.eq(f'{database_single}')], x='conv', y='percentage', color='label'
    #,text='time'
    , orientation='v', title='Laughs Relative Duration per interaction',labels={"conv":"Interaction",
    "percentage":"Percentage difference","label":"Intensity"},trendline='rolling',trendline_options=dict(window=2))
            
    # fig1.show()
    # fig2.show()
    L = [fig1, fig1_1, fig2, fig2_2]
    queue.put(L)       
        
