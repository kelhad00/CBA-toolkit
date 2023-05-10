import os, sys, json
script_path = os.path.realpath(os.path.dirname("IBPY_files"))
os.chdir(script_path)
sys.path.append("..")

import matplotlib.pyplot as plt
import seaborn as sn
import plotly.express as px
import plotly.graph_objects as pg
from plotly.subplots import make_subplots
from .snl_stats_extraction_data import *
from IBPY_files.extract_data import *
from IBPY_files.visualization import *
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

#Until #Mimicry, all the functions below are plotting exactly what its written just after "plot_" in their names.

#Barplots___________________________________________________________
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

        dg1=get_db_from_func_no_pair(DIR,eval("get_laughs_dict_folder"))
        labels1 = ["low", "medium", "high"]

        dg2=get_db_from_func_no_pair(DIR,eval("get_smiles_dict_folder"))
        labels2 = ["subtle", "low", "medium", "high"] 

        fig1=pg.Figure()
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels1)]
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
        fig1.update_layout(title_text=f'Mean, median and standard deviation on laughs - Absolute Duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Time (ms)",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels1,
            categoryorder='array',
            tickmode='array',
            tickvals=labels1,
            ticktext=labels1
        ))

        fig2=pg.Figure()
        for database in (dg2['database'].unique()):
            df_plot=dg2[dg2['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels2)]
            if choice == 'Mean':
                df_mean = df_plot.groupby('label').mean().reset_index()
                fig2.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
            elif choice == 'Median' : 
                df_median = df_plot.groupby('label').median().reset_index()
                fig2.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
            elif choice == 'Standard deviation' :
                df_std = df_plot.groupby('label').std().reset_index()
                fig2.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
            elif choice == 'Min' :
                df_std = df_plot.groupby('label').min().reset_index()
                fig2.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
            elif choice == 'Max' :
                df_std = df_plot.groupby('label').max().reset_index()
                fig2.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
            else :
                fig2.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                    notched=True, boxmean='sd',
                                    name='database=' + database))

        fig2.update_layout(boxmode='group', xaxis_tickangle=0)
        fig2.update_layout(title_text=f'Mean, median and standard deviation on smiles - Absolute Duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Time (ms)",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels2,
            categoryorder='array',
            tickmode='array',
            tickvals=labels2,
            ticktext=labels2
        ))

        return fig1, fig2

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

        df1=get_db_from_func_no_pair(DIR,eval("get_laughs_dict_folder"))
        dg1=get_rd_stats(df1)
        dg1=list_to_df(dg1[0], dg1[1])
        labels1 = ["low", "medium", "high"]

        df2=get_db_from_func_no_pair(DIR,eval("get_smiles_dict_folder"))
        dg2=get_rd_stats(df2)
        dg2=list_to_df(dg2[0], dg2[1])
        labels2 = ["low", "medium", "high"]

        fig1 = make_subplots(rows=1, cols=3, subplot_titles=['Standard deviation', 'Mean', 'Median'])
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels1)]
            fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database), row=1, col=1)
            fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database), row=1, col=2)
            fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database), row=1, col=3)
        fig1.update_xaxes(categoryorder='array', categoryarray=labels1, row=1, col=2)
        fig1.update_xaxes(categoryorder='array', categoryarray=labels1, row=1, col=3)
        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'Mean, median and standard deviation on laughs- Relative Duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Percentage",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels1,
            categoryorder='array',
            tickmode='array',
            tickvals=labels1,
            ticktext=labels1,
        ))


        fig2 = make_subplots(rows=1, cols=3, subplot_titles=['Standard deviation', 'Mean', 'Median'])
        for database in (dg2['database'].unique()):
            df_plot=dg2[dg2['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels2)]
            fig2.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database), row=1, col=1)
            fig2.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database), row=1, col=2)
            fig2.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database), row=1, col=3)
        fig2.update_xaxes(categoryorder='array', categoryarray=labels2, row=1, col=2)
        fig2.update_xaxes(categoryorder='array', categoryarray=labels2, row=1, col=3)
        fig2.update_layout(boxmode='group', xaxis_tickangle=0)
        fig2.update_layout(title_text=f'Mean, median and standard deviation on smiles- Relative Duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Percentage",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels2,
            categoryorder='array',
            tickmode='array',
            tickvals=labels2,
            ticktext=labels2,
        ))
    
    return fig1, fig2


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

        labels_laughs = ["low", "medium", "high"]
        labels_smiles = ["subtle", "low", "medium", "high"]

        dg1=get_db_from_func_no_pair(DIR,eval("get_laughs_from_spk_folder"))
        fig1=pg.Figure()
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels_laughs)]
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
        fig1.update_layout(title_text=f'Mean, median and standard deviation for speaker laughs absolute duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Time (ms)",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels_laughs,
            categoryorder='array',
            tickmode='array',
            tickvals=labels_laughs,
            ticktext=labels_laughs
        ))

        dg2=get_db_from_func_no_pair(DIR,eval("get_smiles_from_spk_folder"))
        fig2=pg.Figure()
        for database in (dg2['database'].unique()):
            df_plot=dg2[dg2['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels_smiles)]
            if choice == 'Mean':
                df_mean = df_plot.groupby('label').mean().reset_index()
                fig2.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
            elif choice == 'Median' : 
                df_median = df_plot.groupby('label').median().reset_index()
                fig2.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
            elif choice == 'Standard deviation' :
                df_std = df_plot.groupby('label').std().reset_index()
                fig2.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
            elif choice == 'Min' :
                df_std = df_plot.groupby('label').min().reset_index()
                fig2.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
            elif choice == 'Max' :
                df_std = df_plot.groupby('label').max().reset_index()
                fig2.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
            else :
                fig2.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                    notched=True, boxmean='sd',
                                    name='database=' + database))

        fig2.update_layout(boxmode='group', xaxis_tickangle=0)
        fig2.update_layout(title_text=f'Mean, median and standard deviation for speaker smiles absolute duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Time (ms)",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels_smiles,
            categoryorder='array',
            tickmode='array',
            tickvals=labels_smiles,
            ticktext=labels_smiles
        ))

        return fig1,fig2
        

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

        labels_laughs = ["low", "medium", "high"]
        labels_smiles = ["subtle", "low", "medium", "high"]

        df1=get_db_from_func_no_pair(DIR,eval("get_laughs_from_spk_folder"))
        dg1=get_rd_stats_byrole(df1)
        dg1=list_to_df(dg1[0], dg1[1])
        fig1 = make_subplots(rows=1, cols=3, subplot_titles=['Standard deviation', 'Mean', 'Median'])
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels_laughs)]
            fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database), row=1, col=1)
            fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database), row=1, col=2)
            fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database), row=1, col=3)
        fig1.update_xaxes(categoryorder='array', categoryarray=labels_laughs, row=1, col=2)
        fig1.update_xaxes(categoryorder='array', categoryarray=labels_laughs, row=1, col=3)
        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'Mean, median and standard deviation for speakers laughs relative duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Percentage",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels_laughs,
            categoryorder='array',
            tickmode='array',
            tickvals=labels_laughs,
            ticktext=labels_laughs
        ))

        df2=get_db_from_func_no_pair(DIR,eval("get_smiles_from_spk_folder"))
        dg2=get_rd_stats_byrole(df2)
        dg2=list_to_df(dg2[0], dg2[1])
        fig2 = make_subplots(rows=1, cols=3, subplot_titles=['Standard deviation', 'Mean', 'Median'])
        for database in (dg2['database'].unique()):
            df_plot=dg2[dg2['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels_smiles)]
            fig2.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database), row=1, col=1)
            fig2.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database), row=1, col=2)
            fig2.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database), row=1, col=3)
        fig2.update_xaxes(categoryorder='array', categoryarray=labels_smiles, row=1, col=2)
        fig2.update_xaxes(categoryorder='array', categoryarray=labels_smiles, row=1, col=3)
        fig2.update_layout(boxmode='group', xaxis_tickangle=0)
        fig2.update_layout(title_text=f'Mean, median and standard deviation for speakers smiles relative duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Percentage",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels_smiles,
            categoryorder='array',
            tickmode='array',
            tickvals=labels_smiles,
            ticktext=labels_smiles
        ))

        return fig1,fig2


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

        labels_laughs = ["low", "medium", "high"]
        labels_smiles = ["subtle", "low", "medium", "high"]

        dg1=get_db_from_func_no_pair(DIR,eval("get_laughs_from_lsn_folder"))
        fig1=pg.Figure()
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels_laughs)]
        
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
        fig1.update_layout(title_text=f'Mean, median and standard deviation for listners laughs absolute duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Time (ms)",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels_laughs,
            categoryorder='array',
            tickmode='array',
            tickvals=labels_laughs,
            ticktext=labels_laughs
        ))

        dg2=get_db_from_func_no_pair(DIR,eval("get_smiles_from_lsn_folder"))
        fig2=pg.Figure()
        for database in (dg2['database'].unique()):
            df_plot=dg2[dg2['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels_smiles)]
            if choice == 'Mean':
                df_mean = df_plot.groupby('label').mean().reset_index()
                fig2.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
            elif choice == 'Median' : 
                df_median = df_plot.groupby('label').median().reset_index()
                fig2.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
            elif choice == 'Standard deviation' :
                df_std = df_plot.groupby('label').std().reset_index()
                fig2.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
            elif choice == 'Min' :
                df_std = df_plot.groupby('label').min().reset_index()
                fig2.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
            elif choice == 'Max' :
                df_std = df_plot.groupby('label').max().reset_index()
                fig2.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
            else :
                fig2.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                    notched=True, boxmean='sd',
                                    name='database=' + database))

        fig2.update_layout(boxmode='group', xaxis_tickangle=0)
        fig2.update_layout(title_text=f'Mean, median and standard deviation for listners smiles absolute duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Time (ms)",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels_smiles,
            categoryorder='array',
            tickmode='array',
            tickvals=labels_smiles,
            ticktext=labels_smiles
        ))

        return fig1, fig2
    


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

        labels_laughs = ["low", "medium", "high"]
        labels_smiles = ["subtle", "low", "medium", "high"]


        df1=get_db_from_func_no_pair(DIR,eval("get_laughs_from_lsn_folder"))
        dg1=get_rd_stats_byrole(df1)
        dg1=list_to_df(dg1[0], dg1[1])

        fig1 = make_subplots(rows=1, cols=3, subplot_titles=['Standard deviation', 'Mean', 'Median'])
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels_laughs)]
            fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database), row=1, col=1)
            fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database), row=1, col=2)
            fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database), row=1, col=3)
        fig1.update_xaxes(categoryorder='array', categoryarray=labels_laughs, row=1, col=2)
        fig1.update_xaxes(categoryorder='array', categoryarray=labels_laughs, row=1, col=3)
        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'Mean, median and standard deviation for listeners laughs relative duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Percentage",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels_laughs,
            categoryorder='array',
            tickmode='array',
            tickvals=labels_laughs,
            ticktext=labels_laughs
        ))

        df2=get_db_from_func_no_pair(DIR,eval("get_smiles_from_lsn_folder"))
        dg2=get_rd_stats_byrole(df2)
        dg2=list_to_df(dg2[0], dg2[1])

        fig2 = make_subplots(rows=1, cols=3, subplot_titles=['Standard deviation', 'Mean', 'Median'])
        for database in (dg2['database'].unique()):
            df_plot=dg2[dg2['database']==database]
            df_plot = df_plot[df_plot['label'].isin(labels_smiles)]
            fig2.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database), row=1, col=1)
            fig2.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database), row=1, col=2)
            fig2.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database), row=1, col=3)
        fig2.update_xaxes(categoryorder='array', categoryarray=labels_smiles, row=1, col=2)
        fig2.update_xaxes(categoryorder='array', categoryarray=labels_smiles, row=1, col=3)
        fig2.update_layout(boxmode='group', xaxis_tickangle=0)
        fig2.update_layout(title_text=f'Mean, median and standard deviation for listeners smiles relative duration', title_x=0.5, 
        xaxis_title="Intensity",
        yaxis_title="Percentage",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels_smiles,
            categoryorder='array',
            tickmode='array',
            tickvals=labels_smiles,
            ticktext=labels_smiles
        ))

        return fig1, fig2



#Scatter plots - Intra _______________________________________________
def plot_intra_absolute_duration(database):
    
    dg = get_db_from_func_no_pair(DIR, get_intra_smiles_absolute_duration_folder)
   
    scatter_fig_smiles=px.scatter(dg[dg.database.eq(f'{database}')], x='subject', y='sum_time', color='label'#,text='time'
    , orientation='v', title='Smiles Absolute Duration - Intra',labels={"sum_time":"Absolute Duration",
    "label":"Intensity"})
    line_fig_smiles=px.line(dg[dg.database.eq(f'{database}')], x='subject', y='sum_time', color='label', symbol='label',
    orientation='v', title='Smiles Absolute Duration - Intra', labels={"sum_time":"Absolute Duration",
    "label":"Intensity"})


    df=get_db_from_func_no_pair(DIR,get_intra_laughs_absolute_duration_folder)
    scatter_fig_laughs=px.scatter(df[df.database.eq(f'{database}')], x='subject', y='sum_time', color='label'#,text='time'
    , orientation='v', title='Laughs Absolute Duration - Intra',labels={"sum_time":"Absolute Duration",
    "label":"Intensity"})
    line_fig_laughs=px.line(df[df.database.eq(f'{database}')], x='subject', y='sum_time', color='label', symbol='label',
    orientation='v', labels={"sum_time":"Absolute Duration", "label":"Intensity"},title='Laughs Absolute Duration - Intra')

    #scatter_fig_smiles.show()
    # fig2.show()
    L= [scatter_fig_smiles, line_fig_smiles, scatter_fig_laughs, line_fig_laughs ]
    return L

def plot_intra_relative_duration(database):
    
    dg = get_db_from_func_no_pair(DIR, get_intra_smiles_relative_duration_folder)

    scatter_fig_smiles=px.scatter(dg[dg.database.eq(f'{database}')], x='subject', y='percentage', color='label',
    orientation='v', title='Smiles Relative Duration - Intra', labels={"label":"Intensity"})
    # fig1=px.scatter(dg, x='subject', y='percentage', color='label',facet_col='database',
    # orientation='v', title='Smiles Relative Duration - Intra', labels={"label":"Intensity"},trendline='rolling',trendline_options=dict(window=5))
    line_fig_smiles=px.line(dg[dg.database.eq(f'{database}')], x='subject', y='percentage', color='label', symbol='label',
    orientation='v', title='Smiles Relative Duration - Intra', labels={"label":"Intensity"})


    df=get_db_from_func_no_pair(DIR, get_intra_laughs_relative_duration_folder)

    scatter_fig_laughs=px.scatter(df[df.database.eq(f'{database}')], x='subject', y='percentage', color='label',
    orientation='v', labels={"label":"Intensity"},title='Laughs Relative Duration - Intra')
    # fig2=px.scatter(df, x='subject', y='percentage', color='label',facet_col='database',
    # orientation='v', labels={"label":"Intensity"},title='Laughs Relative Duration - Intra',trendline='rolling',trendline_options=dict(window=5))
    line_fig_laughs=px.line(df[df.database.eq(f'{database}')], x='subject', y='percentage', color='label', symbol='label',
    orientation='v', labels={"label":"Intensity"},title='Laughs Relative Duration - Intra')

    # scatter_fig_smiles.show()
    # #line_fig_smiles.show()
    # scatter_fig_laughs.show()
    # #line_fig_laughs.show()
    L= [scatter_fig_smiles, line_fig_smiles, scatter_fig_laughs, line_fig_laughs ]
    return L

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
    dg = get_db_from_func_pair(DIR, get_inter_smiles_absolute_duration_folder)

    fig1=px.scatter(dg[dg.database.eq(f'{database}')], x='conv', y='duration', color='label'
    #,text='time'
    , orientation='v', title='Smiles Absolute Duration per interaction',labels={"conv":"Interaction",
    "duration":"Time difference","label":"Intensity"})
    fig1_1=px.scatter(dg[dg.database.eq(f'{database}')], x='conv', y='duration', color='label'
    #,text='time'
    , orientation='v', title='Smiles Absolute Duration per interaction',labels={"conv":"Interaction",
    "duration":"Time difference","label":"Intensity"},trendline='rolling',trendline_options=dict(window=2))

    df = get_db_from_func_pair(DIR, get_inter_laughs_absolute_duration_folder)

    fig2=px.scatter(df[df.database.eq(f'{database}')], x='conv', y='duration', color='label'
    #,text='time'
    , orientation='v', title='Laughs Absolute Duration per interaction',labels={"conv":"Interaction",
    "duration":"Time difference","label":"Intensity"})
    fig2_2=px.scatter(df[df.database.eq(f'{database}')], x='conv', y='duration', color='label'
    #,text='time'
    , orientation='v', title='Laughs Absolute Duration per interaction',labels={"conv":"Interaction",
    "duration":"Time difference","label":"Intensity"},trendline='rolling',trendline_options=dict(window=2))
    
    # #fig1.show()
    # fig1_1.show()
    # #fig2.show()
    # fig2_2.show()
    return [fig1, fig1_1, fig2, fig2_2]

def plot_inter_relative_duration(database):
    dg = get_db_from_func_pair(DIR, get_inter_smiles_relative_duration_folder)

    fig1=px.scatter(dg[dg.database.eq(f'{database}')], x='conv', y='percentage', color='label'
    , orientation='v', title='Smiles Relative Duration per interaction', labels={"conv":"Interaction",
    "percentage":"Percentage difference","label":"Intensity"})
    fig1_1=px.scatter(dg[dg.database.eq(f'{database}')], x='conv', y='percentage', color='label'
    #,text='time'
    , orientation='v', title='Smiles Relative Duration per interaction',labels={"conv":"Interaction",
    "percentage":"Percentage difference","label":"Intensity"},trendline='rolling',trendline_options=dict(window=2))

    df = get_db_from_func_pair(DIR, get_inter_laughs_relative_duration_folder)

    fig2=px.scatter(df[df.database.eq(f'{database}')], x='conv', y='percentage', color='label'
    , orientation='v', labels={"conv":"Interaction","percentage":"Percentage difference",
    "label":"Intensity"},title='Laughs Relative Duration per interaction')
    fig2_2=px.scatter(df[df.database.eq(f'{database}')], x='conv', y='percentage', color='label'
    #,text='time'
    , orientation='v', title='Laughs Relative Duration per interaction',labels={"conv":"Interaction",
    "percentage":"Percentage difference","label":"Intensity"},trendline='rolling',trendline_options=dict(window=2))
    
    # fig1.show()
    # fig2.show()

    return [fig1, fig1_1, fig2, fig2_2]

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


#S&L track - Intra __________________________________________________
def plot_track_previous_SL(dg):
    """Args : The dataframe come from SL_track function"""
    #Previous smiles
    fig=px.bar(dg, x='Trackp', y=['Countp'], color='Databasep', barmode='group',
    text=dg['Percentagep'].apply(lambda x: '{0:1.2f}%'.format(x)) + dg['Countp'].apply(lambda x:'  /  [Count = {0} ]'.format(x)),
    labels={"Trackp": "Previous smiles"},
                title="Tracking Previous Smiles")
    #fig.show()
    return fig

def plot_track_following_SL(dg):
    """Args : The dataframe come from SL_track function"""
    #Following smiles
    fig=px.bar(dg, x='Trackf', y=['Countf'], color='Databasef', barmode='group',
    text=dg['Percentagef'].apply(lambda x: '{0:1.2f}%'.format(x)) + dg['Countf'].apply(lambda x:'  /  [Count = {0} ]'.format(x)),
    labels={"Trackf": "Next smiles"},
                title="Tracking Next Smiles")
    #fig.show()
    return fig

#By intensity
def plot_track_previous_SL_byI(dg):
    """Args : The dataframe comes from SL_track_byI function"""
    #Previous smiles
    fig=px.bar(dg, x='Databasep', y=['Countp'], color='Intensityp', barmode='group', 
    facet_col=dg.iloc[:,2].name,
    text=dg['Percentagep'].apply(lambda x: '{0:1.2f}%'.format(x)) + dg['Countp'].apply(lambda x:'  /  [Count = {0} ]'.format(x)),
    labels={"Intensityp": "Intensity of previous smile"},
                title="Tracking Previous Smiles")
    #fig.show()
    return fig

def plot_track_following_SL_byI(dg):
    """Args : The dataframe come from SL_track_byI function"""
    #Following smiles
    fig=px.bar(dg, x='Databasef', y=['Countf'], color='Intensityf', barmode='group', 
    facet_col=dg.iloc[:,2].name,
    text=dg['Percentagef'].apply(lambda x: '{0:1.2f}%'.format(x)) + dg['Countf'].apply(lambda x:'  /  [Count = {0} ]'.format(x)),
    labels={"Intensityp": "Intensity of next smile"},
                title="Tracking Next Smiles")
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

#Others_______________________________________________________________
def plot_expression_per_min(folder,expression, case=None):
    """This function shows the count of expression we have per minute for smiles or laughs.

    Args:
        folder (list) -> list of all files paths
        expression (str) -> Smiles_0 or Laughs_0
        case (int, optional): Express if you want to look into conversations ; for that, you put 2. Defaults to None.

    Returns:
        Figure: Bar plot
    """
    a=expression_per_min(folder,expression,case)
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
        expression (str) -> Smiles or Laughs
        intensity (str) -> This is the intensity we search. You can type : subtle, low, medium, high for smiles and same for laughs (without subtle)

    Returns:
        Figure: Bar plot
    """
    lst=expression_per_min_I(folder, expression,intensity)
    
    color_lst=["blue",'red','green' , 'purple']
    
    for i in range (len(intensity_smiles)):
        if intensity==intensity_smiles[i]:
            fig = px.bar(x=[_ for _ in range (1,len(lst)+1)], y=lst, color_discrete_sequence =[color_lst[i]]*len(lst) ,
            title=f'Count of {intensity} {expression[:6]} per minute in {get_database_name(folder)}', labels={'x':'Person', 'y':'Count'})
    return fig

