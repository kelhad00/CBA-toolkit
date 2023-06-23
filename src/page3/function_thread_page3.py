import os, sys

script_path=os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")

result_thread=""
import plotly.express as px
from src.snl_stats_extraction_data import *
from IBPY.extract_data import *
from IBPY.visualization import *
DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers=get_parameters()

def create_intra_absolute_plot(database, queue, database_single, expression_choice):
    """ Create intra absolute plot for a given dataset and expression choice.
    
    Args:
        database (str): datasets name
        queue (queue): queue to store the plot
        database_single (str): dataset name choice
        expression_choice (str): expression choice
    Returns:
        list: list of plot + dataframe
    """
    dg=get_db_from_func_no_pair(DIR, get_intra_tiers_absolute_duration_folder, database, expression_choice)
    name_databases=[key.replace('_paths','').upper() for key in databases.keys()]
    databases_=[value for value in databases_pair_paths.values()]
    for i in range(len(name_databases)):
        if database_single==name_databases[i]:
            data_path=databases_[i]
    split_elements=[]
    for i in range(len(data_path)):
        element=data_path[i]
        split_elements.append(os.path.split(element))
    for i in range(len(dg['subject'])):
        if dg['database'][i] == database_single.lower() :
            temp=dg['subject'][i]
            dg['subject'][i]=split_elements[int(temp)-1][-1]
    print(dg)
    scatter_fig_tiers=px.scatter(dg[dg.database.eq(f'{database_single.lower()}')], x='subject', y='sum_time', color='label'#,text='time'
    , orientation='v', title=f'{expression_choice} Absolute Duration - Intra , Database : '+database_single, labels={"sum_time": "Absolute Duration",
    "label": "Entity"})
    scatter_fig_tiers.update_layout(xaxis_title="Files name", yaxis_title="Time (ms)")
    line_fig_tiers=px.line(dg[dg.database.eq(f'{database_single.lower()}')], x='subject', y='sum_time', color='label', symbol='label',
    orientation='v', title=f'{expression_choice} Absolute Duration - Intra , Database : '+database_single, labels={"sum_time": "Absolute Duration",
    "label": "Entity"})
    line_fig_tiers.update_layout(xaxis_title="Files name", yaxis_title="Time (ms)")
    dg = dg.drop('time', axis=1)
    dg = dg.rename(columns={'sum_time': 'duration (ms)', 'label': 'entity', 'subject': 'files name'})
    L=[scatter_fig_tiers, line_fig_tiers, dg]
    queue.put(L)

def create_intra_relative_plot(database, queue, database_single, expression_choice) :
    """ Create intra relative plot for a given dataset and expression choice.
    
    Args:
        database (str): datasets name
        queue (queue): queue to store the plot
        database_single (str): dataset name choice
        expression_choice (str): expression choice
    Returns:
        list: list of plot + dataframe
    """
    dg=get_db_from_func_no_pair(DIR, get_intra_tiers_relative_duration_folder, database, expression_choice)
    name_databases=[key.replace('_paths','').upper() for key in databases.keys()]
    databases_=[value for value in databases_pair_paths.values()]
    for i in range(len(name_databases)):
        if database_single==name_databases[i]:
            data_path=databases_[i]
    split_elements=[]
    for i in range(len(data_path)):
        element=data_path[i]
        split_elements.append(os.path.split(element))
    for i in range(len(dg['subject'])):
        if dg['database'][i] == database_single.lower() :
            temp=dg['subject'][i]
            dg['subject'][i]=split_elements[int(temp)-1][-1]
    scatter_fig_tiers=px.scatter(dg[dg.database.eq(f'{database_single.lower()}')], x='subject', y='percentage', color='label',
    orientation='v', title=f'{expression_choice} Relative Duration - Intra , Database : '+database_single, labels={"label": "Entity"})
    scatter_fig_tiers.update_layout(xaxis_title="Files name", yaxis_title="Percentage (%)")
    line_fig_tiers=px.line(dg[dg.database.eq(f'{database_single.lower()}')], x='subject', y='percentage', color='label', symbol='label',
    orientation='v', title=f'{expression_choice} Relative Duration - Intra , Database : '+database_single, labels={"label": "Entity"})
    line_fig_tiers.update_layout(xaxis_title="Files name", yaxis_title="Percentage (%)")
    dg = dg.rename(columns={'percentage': 'percentage (%)', 'label': 'entity', 'subject': 'files name', 'duration': 'duration of the file (ms)', 'sum_time': 'duration of the entity (ms)'})
    L=[scatter_fig_tiers, line_fig_tiers, dg]
    queue.put(L)

def create_inter_absolute_plot(database, queue, database_single, expression_choice) :
    """ Create inter absolute plot for a given dataset and expression choice.
    
    Args:
        database (str): datasets name
        queue (queue): queue to store the plot
        database_single (str): dataset name choice
        expression_choice (str): expression choice
    Returns:
        list: list of plot + dataframe
    """
    real_tier_lists , real_tiers = get_parameters_tag()
    
    dg=get_db_from_func_pair(DIR, get_inter_tier_absolute_duration_folder, database, expression_choice, real_tier_lists)
    name_databases=[key.replace('_paths','').upper() for key in databases.keys()]
    databases_=[value for value in databases_pair_paths.values()]
    for i in range(len(name_databases)):
        if database_single==name_databases[i]:
            data_path=databases_[i]
    split_elements=[]
    for i in range(len(data_path)):
        element=data_path[i]
        split_elements.append(os.path.split(element))
    for i in range(len(dg['conv'])):
        dg['conv'][i]=dg['conv'][i]-1
    for i in range(len(dg['conv'])):
        if dg['database'][i] == database_single.lower() :
            temp=dg['conv'][i]
            dg['conv'][i]=split_elements[2*int(temp)][-1]+' & '+split_elements[2*int(temp)+1][-1]
    fig1=px.scatter(dg[dg.database.eq(f'{database_single.lower()}')], x='conv', y='duration', color='label'
    , orientation='v', title=f'{expression_choice} Absolute Duration per interaction',labels={"conv": "Interaction",
    "duration": "Time difference","label": "Entity"})
    fig1.update_layout(xaxis_title="Files pairs", yaxis_title="Time (ms)")
    fig1_1=px.line(dg[dg.database.eq(f'{database_single.lower()}')], x='conv', y='duration', color='label', symbol='label'
    , orientation='v', title=f'{expression_choice} Absolute Duration per interaction',labels={"conv": "Pairs files",
    "duration": "Time difference","label": "Entity"})
    fig1_1.update_layout(xaxis_title="Files pairs", yaxis_title="Time (ms)")
    dg = dg.drop('time', axis=1)
    dg = dg.rename(columns={'duration': 'duration (ms)', 'label': 'entity', 'conv': 'files pairs'})
    L=[fig1, fig1_1, dg]
    queue.put(L)

def create_inter_relative_plot(database, queue, database_single, expression_choice) :
    """ Create inter relative plot for a given dataset and expression choice.
    
    Args:
        database (str): datasets name
        queue (queue): queue to store the plot
        database_single (str): dataset name choice
        expression_choice (str): expression choice
    Returns:
        list: list of plot + dataframe
    """
    
    real_tier_lists , real_tiers = get_parameters_tag()
    dg=get_db_from_func_pair(DIR, get_inter_tier_relative_duration_folder, database, expression_choice, real_tier_lists)
    name_databases=[key.replace('_paths','').upper() for key in databases.keys()]
    databases_=[value for value in databases_pair_paths.values()]
    for i in range(len(name_databases)):
        if database_single==name_databases[i]:
            data_path=databases_[i]
    split_elements=[]
    for i in range(len(data_path)):
        element=data_path[i]
        split_elements.append(os.path.split(element))
    for i in range(len(dg['conv'])):
        dg['conv'][i]=dg['conv'][i]-1
    for i in range(len(dg['conv'])):
        if dg['database'][i] == database_single.lower() :
            temp=dg['conv'][i]
            dg['conv'][i]=split_elements[2*int(temp)][-1]+' & '+split_elements[2*int(temp)+1][-1]
    fig1=px.scatter(dg[dg.database.eq(f'{database_single.lower()}')], x='conv', y='percentage', color='label'
    , orientation='v', title=f'{expression_choice} Relative Duration per interaction', labels={"conv": "Interaction",
    "percentage": "Percentage difference","label": "Entity"})
    fig1.update_layout(xaxis_title="Files pairs", yaxis_title="Percentage (%)")
    fig1_1=px.line(dg[dg.database.eq(f'{database_single.lower()}')], x='conv', y='percentage', color='label', symbol='label'
    , orientation='v', title=f'{expression_choice} Relative Duration per interaction',labels={"conv": "Pairs files",
    "percentage": "Percentage difference","label": "Entity"})
    fig1_1.update_layout(xaxis_title="Files pairs", yaxis_title="Percentage (%)")
    dg = dg.rename(columns={'percentage': 'percentage (%)', 'label': 'entity', 'conv': 'files name'})
    L=[fig1, fig1_1, dg]
    queue.put(L)       
        
