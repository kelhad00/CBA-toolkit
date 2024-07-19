import plotly.express as px
from .ml_stats import *

#ML Vizualisation
def plot_element_count(dct):
    """
    The function plot a pie chart of the elements we have in our dictionnary.
    V (list) -> values
    K (list) -> keys
    They have the same length

    Args: 
        dct : dictionnary
    Return:
        A pie chart figure
    """
    K=list(dct.keys())
    V=list(dct.values())

    fig = px.pie(values=V, labels = K, color = K, names=K, title='Occurence of each element of the given list',)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def ML_stats_viz(PATH_IN, PATH_OUT, FRAME_LEN, FRAME_TSTEP, in_out, n, threshold): 
    """This function plot some figures relative to the count of elements we have in our input and output database.

    Args:
        PATH_IN (str):  full input path of eaf datas 
        PATH_OUT (str):  full output path of eaf datas 
        FRAME_LEN (numeric) : Length of a frame (in ms) for one sequence
        FRAME_TSTEP (numeric) : How many ms the frame move between each record
        in_out (numeric): 0 for input and 1 for output
        n (numeric): Number of the video we transformed into frames.
        threshold (numeric): Value for the get_mixedconstant_count function that help to consider a list as constant or not.
        
        For example :
        If in_out = 0 and n = 0, data_in_out[n] represents "input" frames for the video_"0".
    
    Returns:
        fig1 : plot for -> count of elements we have in data_in_out[n]
        fig2 : plot for -> count of mixed and constant elements we have in data_in_out[n]
        fig3 : plot for -> count of elements we have in constant elements of data_in_out[n]
        fig4 : plot for -> count of elements we have in mixed elements of data_in_out[n]

    """
     
    data_in_out = database_creation(PATH_IN, PATH_OUT, FRAME_LEN, FRAME_TSTEP)[in_out]
    get=get_element_count(data_in_out[n])
    get_mc=get_mixedconstant_count(data_in_out[n], threshold)
    constant_lists= get_mc[1][0]
    mixed_lists=get_mc[1][1]
    

    fig1 = plot_element_count(get)      
    fig2 = plot_element_count(get_mc[0]) 
    fig3 = plot_element_count(get_element_count(constant_lists)) 
    fig4 = plot_element_count(get_element_count(mixed_lists)) 

    return fig1, fig2, fig3, fig4

