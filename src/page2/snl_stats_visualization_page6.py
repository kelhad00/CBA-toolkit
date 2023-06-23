import os, sys

script_path=os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")

import plotly.express as px
from src.snl_stats_extraction_data import *
from IBPY.extract_data import *
from IBPY.visualization import *
import numpy as np
DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers=get_parameters()

#Others_______________________________________________________________
def plot_expression_per_min(folder, expression, case=None):
    """ This function shows the count of expression we have per minute.
    
    Args:
        folder (list): list of all files paths
        expression (str): tiers we search
        case (int, optional): express if you want to look into conversations ; for that, you put 2. Defaults to None.
    Returns:
        fig: Bar plot
        df: Dataframe
    """
    a=expression_per_min(folder, expression, case)
    split_elements=[]
    for i in range(len(folder)):
        element=folder[i]
        split_elements.append(os.path.split(element))
    if case is None:
        fig=px.bar(x=[split_elements[i][-1] for i in range(len(split_elements))], y=a[0], title=f'Count of {expression} per minute in {get_database_name(folder)}', 
        labels={'x': 'File', 'y': 'Count'})
    else:
        fig=px.bar(x = [split_elements[j][-1]+' & '+split_elements[j+1][-1] if (j+1) < len(split_elements) else None for j in range(0, len(split_elements), 2)]
        , y=a[0], title=f'Count of {expression} per minute in {get_database_name(folder)}', 
        labels={'x': 'Pairs files', 'y': 'Count'})
    if (np.count_nonzero(fig.data[0]['y'])==0):
        return None
    data = {'Filename': [],'Count': a[0]}
    if case is None:
        data['Filename'] = [split_elements[i][-1] for i in range(len(split_elements))]
    else:
        data['Filename'] = [split_elements[j][-1]+' & '+split_elements[j+1][-1] if (j+1) < len(split_elements) else None for j in range(0, len(split_elements), 2)]
    df = pd.DataFrame(data, columns=['Filename', 'Count'])
    return fig, df

def plot_expression_per_min_I(folder, expression, intensity):
    """ This function shows the count of expression we have per minute for an expression by entity.
    
    Args:
        folder (list): list of all files paths
        expression (str): tiers we search
        intensity (str): this is the entity we search
    Returns:
        fig: Bar plot
    """
    real_tier_lists , real_tiers = get_parameters_tag()

    fig=None
    df=None
    try:
        lst=expression_per_min_I(folder, expression, intensity)
        color_lst=['orange', 'gray', 'white', 'yellow', 'black', 'blue', 'red', 'green', 'purple']
        split_elements=[]
        for i in range(len(folder)):
            element=folder[i]
            split_elements.append(os.path.split(element))
        if all(item == 0 for item in lst):
            fig = None
        else:
            if real_tier_lists[expression]['Replace_Value'] != "" :
                fig=px.bar(x=[split_elements[i][-1] for i in range(len(split_elements))], y=lst, color_discrete_sequence=[color_lst[i]]*len(lst),
                title=f'Count of {intensity} {expression} per minute in {get_database_name(folder)}', labels={'x': 'File', 'y': 'Count'})
            else :
                for i in range (len(real_tier_lists[expression]['Intensities'])):
                    if intensity==real_tier_lists[expression]['Intensities'][i]:
                        fig=px.bar(x=[split_elements[i][-1] for i in range(len(split_elements))], y=lst, color_discrete_sequence=[color_lst[i]]*len(lst),
                        title=f'Count of {intensity} {expression} per minute in {get_database_name(folder)}', labels={'x': 'File', 'y': 'Count'})
        if fig is not None:
            data = {'Filename': [split_elements[i][-1] for i in range(len(split_elements))], 'Count': lst}
            df = pd.DataFrame(data, columns=['Filename', 'Count'])
    except:
        fig=None
    return fig, df
