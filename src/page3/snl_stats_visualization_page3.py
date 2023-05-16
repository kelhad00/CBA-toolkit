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
from .function_thread_page3 import *
from multiprocessing import Queue

#Scatter plots - Intra _______________________________________________
def plot_intra_absolute_duration(database):

    if database != None :

        D = []
        
        for database_single in database : 

            
            dg = get_db_from_func_no_pair(DIR, get_intra_smiles_absolute_duration_folder)
            
            print(dg[dg.database.eq(f'{database_single}')])
            scatter_fig_smiles=px.scatter(dg[dg.database.eq(f'{database_single}')], x='subject', y='sum_time', color='label'#,text='time'
            , orientation='v', title='Smiles Absolute Duration - Intra , Database : ' + database_single,labels={"sum_time":"Absolute Duration",
            "label":"Intensity"})
            line_fig_smiles=px.line(dg[dg.database.eq(f'{database_single}')], x='subject', y='sum_time', color='label', symbol='label',
            orientation='v', title='Smiles Absolute Duration - Intra , Database : ' + database_single, labels={"sum_time":"Absolute Duration",
            "label":"Intensity"})


            df=get_db_from_func_no_pair(DIR,get_intra_laughs_absolute_duration_folder)
            scatter_fig_laughs=px.scatter(df[df.database.eq(f'{database_single}')], x='subject', y='sum_time', color='label'#,text='time'
            , orientation='v', title='Laughs Absolute Duration - Intra , Database : ' + database_single,labels={"sum_time":"Absolute Duration",
            "label":"Intensity"})
            line_fig_laughs=px.line(df[df.database.eq(f'{database_single}')], x='subject', y='sum_time', color='label', symbol='label',
            orientation='v', labels={"sum_time":"Absolute Duration", "label":"Intensity"},title='Laughs Absolute Duration - Intra , Database : '+ database_single)

            #scatter_fig_smiles.show()s
            # fig2.show()
            L= [scatter_fig_smiles, line_fig_smiles, scatter_fig_laughs, line_fig_laughs ]
            D.append(L)
            
        
        return D

def plot_intra_relative_duration(database):
    

    if database != None :

        D = []
       

        for database_single in database : 

            print(database_single)

            dg = get_db_from_func_no_pair(DIR, get_intra_smiles_relative_duration_folder)

            scatter_fig_smiles=px.scatter(dg[dg.database.eq(f'{database_single}')], x='subject', y='percentage', color='label',
            orientation='v', title='Smiles Relative Duration - Intra , Database : ' + database_single, labels={"label":"Intensity"})
            # fig1=px.scatter(dg, x='subject', y='percentage', color='label',facet_col='database',
            # orientation='v', title='Smiles Relative Duration - Intra', labels={"label":"Intensity"},trendline='rolling',trendline_options=dict(window=5))
            line_fig_smiles=px.line(dg[dg.database.eq(f'{database_single}')], x='subject', y='percentage', color='label', symbol='label',
            orientation='v', title='Smiles Relative Duration - Intra , Database : ' + database_single, labels={"label":"Intensity"})


            df=get_db_from_func_no_pair(DIR, get_intra_laughs_relative_duration_folder)

            scatter_fig_laughs=px.scatter(df[df.database.eq(f'{database_single}')], x='subject', y='percentage', color='label',
            orientation='v', labels={"label":"Intensity"},title='Laughs Relative Duration - Intra , Database : ' + database_single)
            # fig2=px.scatter(df, x='subject', y='percentage', color='label',facet_col='database',
            # orientation='v', labels={"label":"Intensity"},title='Laughs Relative Duration - Intra',trendline='rolling',trendline_options=dict(window=5))
            line_fig_laughs=px.line(df[df.database.eq(f'{database_single}')], x='subject', y='percentage', color='label', symbol='label',
            orientation='v', labels={"label":"Intensity"},title='Laughs Relative Duration - Intra , Database : ' + database_single)
            # scatter_fig_smiles.show()
            # #line_fig_smiles.show()
            # scatter_fig_laughs.show()
            # #line_fig_laughs.show()
            L= [scatter_fig_smiles, line_fig_smiles, scatter_fig_laughs, line_fig_laughs ]
            
            D.append(L)
        
        return D

#Filter by role
def plot_absolute_duration_from_lsn_folder(listpaths,string):
    
    dg1=get_intra_smiles_ad_from_lsn_folder(listpaths,string)
    dg2=get_intra_laughs_ad_from_lsn_folder(listpaths,string)
    dg1=list_to_df(dg1[0], dg1[1])
    dg2=list_to_df(dg2[0], dg2[1])


    fig1=px.scatter(dg1, x='subject', y='sum_time', color='label',
    title=f"Smiles absolute duration for {string} database - For listeners")
    #,text='time', orientation='v')
    #fig1.show()

    fig2=px.scatter(dg2, x='subject', y='sum_time', color='label',
    title=f"Laughs absolute duration for {string} database - For listeners")
    #,text='time', orientation='v')
    #fig2.show()

    L=[fig1, fig2]
    return L

def plot_absolute_duration_from_spk_folder(listpaths,string):
    dg1=get_intra_smiles_ad_from_spk_folder(listpaths,string)
    dg2=get_intra_laughs_ad_from_spk_folder(listpaths,string)
    dg1=list_to_df(dg1[0], dg1[1])
    dg2=list_to_df(dg2[0], dg2[1])


    fig1=px.scatter(dg1, x='subject', y='sum_time', color='label',
    title=f"Smiles absolute duration for {string} database - For speakers")
    #,text='time', orientation='v')
    #fig1.show()

    fig2=px.scatter(dg2, x='subject', y='sum_time', color='label',
    title=f"Laughs absolute duration for {string} database - For speakers")
    #,text='time', orientation='v')
    #fig2.show()
    L=[fig1, fig2]
    return L

def plot_relative_duration_from_lsn_folder(listpaths,string):
    dg1=get_intra_smiles_rd_from_lsn_folder(listpaths,string)
    dg2=get_intra_laughs_rd_from_lsn_folder(listpaths,string)
    dg1=list_to_df(dg1[0], dg1[1])
    dg2=list_to_df(dg2[0], dg2[1])

    fig1=px.scatter(dg1, x='subject', y='percentage', color='label', 
    title=f"Smiles relative duration for {string} database - For listeners")
    #,text=dg1['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), orientation='v')
    #fig1.show()

    fig2=px.scatter(dg2, x='subject', y='percentage', color='label', 
    title=f"Laughs relative duration for {string} database - For listeners")
    #,text=dg2['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), orientation='v')
    #fig2.show()
    L=[fig1, fig2]
    return L

def plot_relative_duration_from_spk_folder(listpaths,string):
    dg1=get_intra_smiles_rd_from_spk_folder(listpaths,string)
    dg2=get_intra_laughs_rd_from_spk_folder(listpaths,string)
    dg1=list_to_df(dg1[0], dg1[1])
    dg2=list_to_df(dg2[0], dg2[1])

    fig1=px.scatter(dg1, x='subject', y='percentage', color='label', 
    title=f"Smiles relative duration for {string} database - For speakers")
    #,text=dg1['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), orientation='v')
    #fig1.show()

    fig2=px.scatter(dg2, x='subject', y='percentage', color='label', 
    title=f"Laughs relative duration for {string} database - For speakers")
    #,text=dg2['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), orientation='v')
    #fig2.show()
    
    L=[fig1, fig2]

    return L


#Scatter plots - Inter _______________________________________________
def plot_inter_absolute_duration(database):


    if database != None :

        D=[]
        Thread = []
        queue = Queue()

        for database_single in database : 
   
            Thread.append(threading.Thread(target=create_inter_absolute_plot, args=(database_single,queue,)))

        for thread in Thread :

            thread.start()

        for thread in Thread :
            
            thread.join()
            D.append(queue.get())

        return D

def plot_inter_relative_duration(database):

    if database != None :

        D=[]
        Thread = []
        queue = Queue()

        for database_single in database : 
             
            Thread.append(threading.Thread(target=create_inter_relative_plot, args=(database_single,queue,)))
            
        for thread in Thread :

            thread.start()
        
        for thread in Thread : 

            thread.join()
            D.append(queue.get())

        return D
            

#Filter by Roles
def plot_inter_ad_spk_vs_lsn(database):
    
    df = get_db_from_func_pair(DIR, get_inter_smiles_ad_spk_vs_lsn_folder)
    fig1=px.scatter(df[df.database.eq(f'{database}')], x='conv', y='sum_time', color='label', symbol='role'
    #,text='time'
    , orientation='v', title='Smiles Absolute Duration - Speaker vs Listner',labels={"conv":"Interaction",
    "sum_time":"Absolute Duration","label":"Intensity"})

    dg = get_db_from_func_pair(DIR, get_inter_laughs_ad_spk_vs_lsn_folder)
    fig2=px.scatter(dg[dg.database.eq(f'{database}')], x='conv', y='sum_time', color='label', symbol='role'
    #,text='time'
    , orientation='v', title='Laughs Absolute Duration - Speaker vs Listner',labels={"conv":"Interaction",
    "sum_time":"Absolute Duration","label":"Intensity"})

    # fig1.show()
    # fig2.show()
    return [fig1, fig2]

def plot_inter_rd_spk_vs_lsn(database):
    df = get_db_from_func_pair(DIR, get_inter_smiles_rd_spk_vs_lsn_folder)
    fig1=px.scatter(df[df.database.eq(f'{database}')], x='conv', y='percentage', color='label',symbol='role'
    #,text='time'
    , orientation='v', title='Smiles Relative Duration - Speaker vs Listner',labels={"conv":"Interaction",
    "percentage":"Percentage","label":"Intensity"})

    dg = get_db_from_func_pair(DIR, get_inter_laughs_rd_spk_vs_lsn_folder)
    fig2=px.scatter(dg[dg.database.eq(f'{database}')], x='conv', y='percentage', color='label', symbol='role'
    #,text='time'
    , orientation='v', title='Laughs Relative Duration - Speaker vs Listner',labels={"conv":"Interaction",
    "percentage":"Percentage","label":"Intensity"})

    # fig1.show()
    # fig2.show()
    return [fig1, fig2]

def plot_inter_ad_lsn_vs_spk(database):
    df = get_db_from_func_pair(DIR, get_inter_smiles_ad_lsn_vs_spk_folder)
    fig1=px.scatter(df[df.database.eq(f'{database}')], x='conv', y='sum_time', color='label', symbol='role'
    #,text='time'
    , orientation='v', title='Smiles Absolute Duration - Listner vs Speaker',labels={"conv":"Interaction",
    "sum_time":"Absolute Duration","label":"Intensity"})

    dg = get_db_from_func_pair(DIR, get_inter_laughs_ad_lsn_vs_spk_folder)
    fig2=px.scatter(dg[dg.database.eq(f'{database}')], x='conv', y='sum_time', color='label', symbol='role'
    #,text='time'
    , orientation='v', title='Laughs Absolute Duration - Listner vs Speaker',labels={"conv":"Interaction",
    "sum_time":"Absolute Duration","label":"Intensity"})

    # fig1.show()
    # fig2.show()
    return [fig1, fig2]

def plot_inter_rd_lsn_vs_spk(database):
    df = get_db_from_func_pair(DIR, get_inter_smiles_rd_lsn_vs_spk_folder)    
    fig1=px.scatter(df[df.database.eq(f'{database}')], x='conv', y='percentage', color='label', symbol='role'
    #,text='time'
    , orientation='v', title='Smiles Relative Duration - Listner vs Speaker',labels={"conv":"Interaction",
    "percentage":"Percentage","label":"Intensity"})

    dg = get_db_from_func_pair(DIR, get_inter_laughs_rd_lsn_vs_spk_folder)    
    fig2=px.scatter(dg[dg.database.eq(f'{database}')], x='conv', y='percentage', color='label', symbol='role'
    #,text='time'
    , orientation='v', title='Laughs Relative Duration - Listner vs Speaker',labels={"conv":"Interaction",
    "percentage":"Percentage","label":"Intensity"})

    # fig1.show()
    # fig2.show()
    return [fig1, fig2]
