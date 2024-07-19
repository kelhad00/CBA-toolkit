import os, sys

script_path=os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")

import plotly.graph_objects as pg
from src.snl_stats_extraction_data import *
from IBPY.extract_data import *
from IBPY.visualization import *
DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers=get_parameters()
real_tier_lists , real_tiers = get_parameters_tag()

def create_plot_absolute_duration_thread(Tiers, choice, queue, name_databases) :

    real_tier_lists , real_tiers = get_parameters_tag()
    ''' Create a plot of the absolute duration of the tiers in the dataset.
    
    Args:
        Tiers (str): The tier to plot
        choice (str): The choice of the user between Mean, Median and Standard deviation, Min, Max
        queue (Queue): The queue to send the plot
        name_databases (list): The list of the datasets
    Returns:
        A plot of the absolute duration of the tiers in the dataset
    '''
    try :
        dg1=get_db_from_func_no_pair(DIR, eval("get_tier_dict_folder"), name_databases, Tiers)
        fig1=pg.Figure()
        if not dg1.empty:
            if real_tier_lists[Tiers]['Replace_Value'] != "" :
                labels=[real_tier_lists[Tiers]['Replace_Value'], "No_"+real_tier_lists[Tiers]['Replace_Value']]
            else :
                labels = real_tier_lists[Tiers]['Intensities']
            for database in (dg1['database'].unique()):
                df_plot=dg1[dg1['database']==database]
                df_plot=df_plot[df_plot['label'].isin(labels)]
                if not df_plot.empty:
                    if choice=='Mean':
                        df_mean=df_plot.groupby('label').mean(numeric_only=True).reset_index()
                        fig1.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
                    elif choice=='Median': 
                        df_median = df_plot.groupby('label').median(numeric_only=True).reset_index()
                        fig1.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
                    elif choice=='Standard deviation':
                        df_std=df_plot.groupby('label').std(numeric_only=True).reset_index()
                        fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                    elif choice=='Min':
                        df_std=df_plot.groupby('label').min(numeric_only=True).reset_index()
                        fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                    elif choice=='Max':
                        df_std=df_plot.groupby('label').max(numeric_only=True).reset_index()
                        fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                    else:
                        fig1.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                            notched=True, boxmean='sd',
                                            name='database='+database))
            fig1.update_layout(boxmode='group', xaxis_tickangle=0)
            fig1.update_layout(title_text=f'{choice} on {Tiers} - Absolute Duration', title_x=0.5, 
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
        else:
            fig1=None
    except:
        fig1=None
    queue.put(fig1)

def create_plot_relative_duration_thread(Tiers, choice, queue, database_names) :
    ''' Create a plot of the relative duration of the tiers in the dataset.

    Args:
        Tiers (str): The tier to plot
        choice (str): The choice of the user between Mean, Median and Standard deviation, Min, Max
        queue (Queue): The queue to send the plot
        database_names (list): The list of the datasets
    Returns:
        A plot of the relative duration of the tiers in the dataset
    '''
    real_tier_lists , real_tiers = get_parameters_tag()

    try :
        df1=get_db_from_func_no_pair(DIR, eval("get_tier_dict_folder"), database_names, Tiers)
        if not df1.empty:
            dg1=get_rd_stats(df1)
            dg1=list_to_df(dg1[0], dg1[1])
            if real_tier_lists[Tiers]['Replace_Value'] != "" :
                labels=[real_tier_lists[Tiers]['Replace_Value'], "No_"+real_tier_lists[Tiers]['Replace_Value']]
            else :
                labels = real_tier_lists[Tiers]['Intensities']    
            fig1=pg.Figure()
            for database in (dg1['database'].unique()):
                df_plot=dg1[dg1['database']==database]
                df_plot=df_plot[df_plot['label'].isin(labels)]
                if choice=='Mean':
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database))
                elif choice=='Median': 
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database))
                elif choice=='Standard deviation':
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database))
                elif choice=='Min':
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name=database))
                elif choice=='Max':
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name=database))
                else:
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name='Mean '+database))
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name='Median '+database))
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name='Standard deviation '+database))
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name='Min '+database))
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name='Max '+database))
            fig1.update_layout(boxmode='group', xaxis_tickangle=0)
            fig1.update_layout(title_text=f'{choice} on {Tiers} - Relative Duration', title_x=0.5, 
            xaxis_title="Entity",
            yaxis_title="Percentage (%)",
            legend_title="Datasets",
            xaxis=dict(
                categoryarray=labels,
                categoryorder='array',
                tickmode='array',
                tickvals=labels,
                ticktext=labels,
            ))
        else:
            fig1=None
    except:
        fig1=None
    queue.put(fig1)
    
#Filter by role   
def create_absolute_duration_from_spk_thread(Tiers, choice, queue, name_databases) :
    ''' Create a plot of the absolute duration of the tiers in the dataset filtered by role of the speaker.
    
    Args:
        Tiers (str): The tier to plot
        choice (str): The choice of the user between Mean, Median and Standard deviation, Min, Max
        queue (Queue): The queue to send the plot
        name_databases (list): The list of the datasets
    Returns:
        A plot of the absolute duration of the tiers in the dataset filtered by role of the speaker
    '''
    labels=real_tier_lists[Tiers]['Intensities']   
    dg1=get_db_from_func_no_pair(DIR,eval("get_tier_from_spk_folder"), name_databases, Tiers)
    fig1=pg.Figure()
    if not dg1.empty:
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot=df_plot[df_plot['label'].isin(labels)]
            if not df_plot.empty:
                if choice=='Mean':
                    df_mean=df_plot.groupby('label').mean().reset_index()
                    fig1.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
                elif choice=='Median': 
                    df_median=df_plot.groupby('label').median().reset_index()
                    fig1.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
                elif choice=='Standard deviation':
                    df_std=df_plot.groupby('label').std().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice=='Min':
                    df_std=df_plot.groupby('label').min().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice=='Max':
                    df_std=df_plot.groupby('label').max().reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                else:
                    fig1.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                        notched=True, boxmean='sd',
                                        name='database='+database))
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
    else:
        fig1=None

    queue.put(fig1)

def create_relative_duration_from_spk_thread(Tiers, choice, queue, name_databases) :
    ''' Create a plot of the relative duration of the tiers in the dataset filtered by role of the speaker.
    
    Args:
        Tiers (str): The tier to plot
        choice (str): The choice of the user between Mean, Median and Standard deviation, Min, Max
        queue (Queue): The queue to send the plot
        name_databases (list): The list of the datasets
    Returns:
        A plot of the relative duration of the tiers in the dataset filtered by role of the speaker
    '''
    labels=real_tier_lists[Tiers]['Intensities']    
    df1=get_db_from_func_no_pair(DIR,eval("get_tier_from_spk_folder"), name_databases, Tiers)
    if not df1.empty:
        dg1=get_rd_stats_byrole(df1)
        dg1=list_to_df(dg1[0], dg1[1])
        fig1=pg.Figure()
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot=df_plot[df_plot['label'].isin(labels)]
            if choice=='Mean':
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database))
            elif choice=='Median': 
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database))
            elif choice=='Standard deviation':
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database))
            elif choice=='Min':
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name=database))
            elif choice=='Max':
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name=database))
            else:
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name='Mean '+database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name='Median '+database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name='Standard deviation '+database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name='Min '+database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name='Max '+database))
        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'{choice} for speakers on {Tiers} - Relative duration', title_x=0.5, 
        xaxis_title="Entity",
        yaxis_title="Percentage (%)",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels,
            categoryorder='array',
            tickmode='array',
            tickvals=labels,
            ticktext=labels
        ))
    else:
        fig1=None

    queue.put(fig1)

def create_absolute_duration_from_lsn_thread(Tiers, choice, queue, name_databases) :
    ''' Create a plot of the absolute duration of the tiers in the dataset filtered by role of the listener.

    Args:
        Tiers (str): The tier to plot
        choice (str): The choice of the user between Mean, Median and Standard deviation, Min, Max
        queue (Queue): The queue to send the plot
        name_databases (list): The list of the datasets
    Returns:
        A plot of the absolute duration of the tiers in the dataset filtered by role of the listener
    '''
    labels=real_tier_lists[Tiers]['Intensities']   
    dg1=get_db_from_func_no_pair(DIR,eval("get_tier_from_lsn_folder"), name_databases, Tiers)
    fig1=pg.Figure()
    if not dg1.empty:
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot=df_plot[df_plot['label'].isin(labels)]
            if not df_plot.empty:
                if choice=='Mean':
                    df_mean=df_plot.groupby('label').mean(numeric_only=True).reset_index()
                    fig1.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
                elif choice=='Median': 
                    df_median=df_plot.groupby('label').median(numeric_only=True).reset_index()
                    fig1.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
                elif choice=='Standard deviation':
                    df_std=df_plot.groupby('label').std(numeric_only=True).reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice=='Min':
                    df_std=df_plot.groupby('label').min(numeric_only=True).reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                elif choice=='Max':
                    df_std=df_plot.groupby('label').max(numeric_only=True).reset_index()
                    fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                else:
                    fig1.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                        notched=True, boxmean='sd',
                                        name='database='+database))
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
    else:
        fig1=None

    queue.put(fig1)
  
def create_relative_duration_from_lsn_thread(Tiers, choice, queue, name_databases) :
    ''' Create a plot of the relative duration of the tiers in the dataset filtered by role of the listener.
    
    Args:
        Tiers (str): The tier to plot
        choice (str): The choice of the user between Mean, Median and Standard deviation, Min, Max
        queue (Queue): The queue to send the plot
        name_databases (list): The list of the datasets
    Returns:
        A plot of the relative duration of the tiers in the dataset filtered by role of the listener
    '''
    labels=real_tier_lists[Tiers]['Intensities']    
    df1=get_db_from_func_no_pair(DIR,eval("get_tier_from_lsn_folder"), name_databases, Tiers)
    if not df1.empty:
        dg1=get_rd_stats_byrole(df1)
        dg1=list_to_df(dg1[0], dg1[1])
        fig1=pg.Figure()
        for database in (dg1['database'].unique()):
            df_plot=dg1[dg1['database']==database]
            df_plot=df_plot[df_plot['label'].isin(labels)]
            if choice=='Mean':
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database))
            elif choice=='Median': 
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database))
            elif choice=='Standard deviation':
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database))
            elif choice=='Min':
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name=database))
            elif choice=='Max':
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name=database))
            else:
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name='Mean '+database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name='Median '+database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name='Standard deviation '+database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name='Min '+database))
                fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name='Max '+database))
        fig1.update_layout(boxmode='group', xaxis_tickangle=0)
        fig1.update_layout(title_text=f'{choice} for listeners on {Tiers} - Relative duration', title_x=0.5, 
        xaxis_title="Entity",
        yaxis_title="Percentage (%)",
        legend_title="Datasets",
        xaxis=dict(
            categoryarray=labels,
            categoryorder='array',
            tickmode='array',
            tickvals=labels,
            ticktext=labels
        ))   
    else:
       fig1=None

    queue.put(fig1)

#Filter by tier 
def create_absolute_duration_from_tier_thread(Tiers, choice, queue, name_databases, tier1, entity) :
    ''' Create a graph with the absolute duration of the entity in the tier filtered by another tier.
    
    Args:
        Tiers (str): the tier to filter
        choice (str): the choice of the user
        queue (queue): the queue to put the graph
        name_databases (list): the list of the datasets
        tier1 (str): the tier used to filter
        entity (str): the entity of the tier
    Returns:
        fig1 (plotly.graph_objects.Figure): the graph
    '''
    real_tier_lists , real_tiers = get_parameters_tag()

    try :
        if real_tier_lists[Tiers]['Replace_Value'] != "" :
                labels=[real_tier_lists[Tiers]['Replace_Value'], str("No_"+real_tier_lists[Tiers]['Replace_Value'])]
        else :
            labels = real_tier_lists[Tiers]['Intensities']    
        dg1=get_db_from_func_no_pair_tier(DIR,eval("get_tier_from_tier"), name_databases, tier1, Tiers, entity)
        fig1=pg.Figure()
        if not dg1.empty:
            for database in (dg1['database'].unique()):
                df_plot=dg1[dg1['database']==database]
                df_plot=df_plot[df_plot['label'].isin(labels)]
                if not df_plot.empty:
                    if choice=='Mean':
                        df_mean=df_plot.groupby('label').mean(numeric_only=True).reset_index()
                        fig1.add_trace(pg.Bar(x=df_mean.label, y=df_mean.diff_time, name=database))
                    elif choice=='Median': 
                        df_median=df_plot.groupby('label').median(numeric_only=True).reset_index()
                        fig1.add_trace(pg.Bar(x=df_median.label, y=df_median.diff_time, name=database))
                    elif choice=='Standard deviation':
                        df_std = df_plot.groupby('label').std(numeric_only=True).reset_index()
                        fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                    elif choice=='Min':
                        df_std=df_plot.groupby('label').min(numeric_only=True).reset_index()
                        fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                    elif choice=='Max':
                        df_std=df_plot.groupby('label').max(numeric_only=True).reset_index()
                        fig1.add_trace(pg.Bar(x=df_std.label, y=df_std.diff_time, name=database))
                    else:
                        fig1.add_trace(pg.Box(x=df_plot.label, y=df_plot.diff_time,
                                            notched=True, boxmean='sd',
                                            name='database='+database))
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
        else:
            fig1=None
    except:
        fig1=None
    queue.put(fig1)

def create_relative_duration_from_tier_thread(Tiers, choice, queue, name_databases, tier1, entity) :
    ''' Create a graph with the relative duration of the entity in the tier filtered by another tier.
    
    Args:
        Tiers (str): the tier to filter
        choice (str): the choice of the user
        queue (queue): the queue to put the graph
        name_databases (list): the list of the datasets
        tier1 (str): the tier used to filter
        entity (str): the entity of the tier
    Returns:
        fig1 (plotly.graph_objects.Figure): the graph
    '''
    try :
        
        if real_tier_lists[Tiers]['Replace_Value'] != "" :
                labels=[real_tier_lists[Tiers]['Replace_Value'], str("No_"+real_tier_lists[Tiers]['Replace_Value'])]
        else :
            labels = real_tier_lists[Tiers]['Intensities'] 
        df1=get_db_from_func_no_pair_tier(DIR,eval("get_tier_from_tier"), name_databases, tier1, Tiers, entity)
        if not df1.empty:
            dg1=get_rd_stats_byrole(df1)
            dg1=list_to_df(dg1[0], dg1[1])
            fig1=pg.Figure()
            for database in (dg1['database'].unique()):
                df_plot=dg1[dg1['database']==database]
                df_plot=df_plot[df_plot['label'].isin(labels)]
                if choice=='Mean':
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name=database))
                elif choice=='Median': 
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name=database))
                elif choice=='Standard deviation':
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name=database))
                elif choice=='Min':
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name=database))
                elif choice=='Max':
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name=database))
                else:
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.mean_p, name='Mean '+database))
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.median_p, name='Median '+database))
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.std_p, name='Standard deviation '+database))
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.min_p, name='Min '+database))
                    fig1.add_trace(pg.Bar(x=df_plot.label, y=df_plot.max_p, name='Max '+database))
            fig1.update_layout(boxmode='group', xaxis_tickangle=0)
            fig1.update_layout(title_text=f'{choice} for {entity} {tier1} on {Tiers} - Relative duration', title_x=0.5, 
            xaxis_title="Entity",
            yaxis_title="Percentage (%)",
            legend_title="Datasets",
            xaxis=dict(
                categoryarray=labels,
                categoryorder='array',
                tickmode='array',
                tickvals=labels,
                ticktext=labels
            ))   
        else:
            fig1=None
    except:
        fig1=None
    queue.put(fig1)