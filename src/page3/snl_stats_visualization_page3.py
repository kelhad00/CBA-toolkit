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
def plot_intra_absolute_duration(database, expression_choice):
    if database != None :

        D = []
        Threads = []
        queue = Queue()

        for database_single in database:
            Threads.append(threading.Thread(target=create_intra_absolute_plot(database, queue, database_single, expression_choice)))
            
        for thread in Threads:

            thread.start()

        for thread in Threads:

            thread.join()
            D.append(queue.get())
            
        
        return D

def plot_intra_relative_duration(database, expression_choice):
    

    if database != None :

        D = []
        Threads = []
        queue = Queue()

        for database_single in database:
            Threads.append(threading.Thread(target=create_intra_relative_plot, args=(database, queue, database_single, expression_choice)))

        for thread in Threads:

            thread.start()
        
        for thread in Threads:

            thread.join()
            D.append(queue.get())
           
    return D

#Filter by tier
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

def plot_absolute_duration_from_tier_folder(listpaths, string, tier1, tier2, entity):

    dg1=get_intra_tier_ad_from_tier_folder(listpaths,string, tier1, tier2, entity)
    dg1=list_to_df(dg1[0], dg1[1])

    split_elements = []

    for i in range(len(listpaths)) :
        element = listpaths[i]
        split_elements.append(element.split('\\'))

    for i in range(len(dg1['subject'])) :

        temp = dg1['subject'][i]
        dg1['subject'][i] = split_elements[int(temp)-1][-1]

    fig1=px.scatter(dg1, x='subject', y='sum_time', color='label',
    title=f"{tier2} absolute duration for {string} database - For {entity} {tier1}")
    fig1.update_layout(xaxis_title="Files name", yaxis_title="Time (ms)")

    L=[fig1]
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

def plot_relative_duration_from_tier_folder(listpaths, string, tier1, tier2, entity):


    dg1=get_intra_tier_rd_from_tier_folder(listpaths,string, tier1, tier2, entity)
    dg1=list_to_df(dg1[0], dg1[1])

    split_elements = []

    for i in range(len(listpaths)) :
        element = listpaths[i]
        split_elements.append(element.split('\\'))

    for i in range(len(dg1['subject'])) :

        temp = dg1['subject'][i]
        dg1['subject'][i] = split_elements[int(temp)-1][-1]
        

    fig1=px.scatter(dg1, x='subject', y='percentage', color='label', 
    title=f"{tier2} relative duration for {string} database - For {entity} {tier1}")
    fig1.update_layout(xaxis_title="Files name", yaxis_title="Percentage (%)")

    L=[fig1]
    return L

#Scatter plots - Inter _______________________________________________
def plot_inter_absolute_duration(database, expression_choice):


    if database != None :

        D=[]
        Thread = []
        queue = Queue()

        for database_single in database : 
   
            Thread.append(threading.Thread(target=create_inter_absolute_plot, args=(database, queue, database_single, expression_choice)))

        for thread in Thread :

            thread.start()

        for thread in Thread :
            
            thread.join()
            D.append(queue.get())

        return D

def plot_inter_relative_duration(database, expression_choice):

    if database != None :

        D=[]
        Thread = []
        queue = Queue()

        for database_single in database : 
             
            Thread.append(threading.Thread(target=create_inter_relative_plot, args=(database, queue, database_single, expression_choice)))
            
        for thread in Thread :

            thread.start()
        
        for thread in Thread : 

            thread.join()
            D.append(queue.get())

        return D
            

#Filter by Roles
def plot_inter_ad_spk_vs_lsn(database):
    
    df = get_db_from_func_pair(DIR, get_inter_smiles_ad_spk_vs_lsn_folder)
    # df = get_db_from_func_pair(DIR, get_inter_tier_ad_entity1_vs_entity2_folder, database, expression_choice, tier_lists)

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

#Filter by Tiers
def plot_inter_ad_entity1_vs_entity2_tier(database, tier1, tier2, entity1, entity2):

    df = get_db_from_func_pair_tier(DIR, get_inter_tier_ad_entity1_vs_entity2_folder, database, tier1, tier2, entity1, entity2)

    name_databases = [key.split('_')[0].upper() for key in databases.keys()]
    databases_ = [value for value in databases_pair_paths.values()]

    for i in range(len(name_databases)):
        if database==name_databases[i]:
            data_path=databases_[i]

    split_elements = []

    for i in range(len(data_path)) :
        element = data_path[i]
        split_elements.append(element.split('\\'))

    for i in range(len(df['conv'])) :

        df['conv'][i] = df['conv'][i]-1

    for i in range(len(df['conv'])) :

        temp = df['conv'][i]
        df['conv'][i] = split_elements[2*int(temp)][-1] + ' & ' + split_elements[2*int(temp) + 1][-1]

    fig1=px.scatter(df[df.database.eq(f'{database.lower()}')], x='conv', y='sum_time', color='label', symbol='role'
    #,text='time'
    , orientation='v', title=f'{tier2} Absolute Duration - {entity1} vs {entity2} {tier1}',labels={"conv":"Pairs files",
    "sum_time":"Absolute Duration","label":f"Entity of {tier2}", "role":f"Entity of {tier1}"})
    fig1.update_layout(xaxis_title="Files pairs", yaxis_title="Time (ms)")
    return [fig1]

def plot_inter_rd_entity1_vs_entity2_tier(database, tier1, tier2, entity1, entity2):
    
    df = get_db_from_func_pair_tier(DIR, get_inter_tier_rd_entity1_vs_entity2_folder, database, tier1, tier2, entity1, entity2)

    name_databases = [key.split('_')[0].upper() for key in databases.keys()]
    databases_ = [value for value in databases_pair_paths.values()]

    for i in range(len(name_databases)):
        if database==name_databases[i]:
            data_path=databases_[i]

    split_elements = []

    for i in range(len(data_path)) :
        element = data_path[i]
        split_elements.append(element.split('\\'))

    for i in range(len(df['conv'])) :

        df['conv'][i] = df['conv'][i]-1

    for i in range(len(df['conv'])) :

        temp = df['conv'][i]
        df['conv'][i] = split_elements[2*int(temp)][-1] + ' & ' + split_elements[2*int(temp) + 1][-1]

    fig1=px.scatter(df[df.database.eq(f'{database.lower()}')], x='conv', y='percentage', color='label', symbol='role'
    #,text='time'
    , orientation='v', title=f'{tier2} Relative Duration - {entity1} vs {entity2} {tier1}',labels={"conv":"Pairs files",
    "percentage":"Percentage","label":f"Entity of {tier2}", "role":f"Entity of {tier1}"})
    fig1.update_layout(xaxis_title="Files pairs", yaxis_title="Percentage (%)")

    # fig1.show()
    # fig2.show()
    return [fig1]
