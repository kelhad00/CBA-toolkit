import streamlit as st
import os, sys, json
import Affichage_pattern
script_path = os.path.realpath(os.path.dirname("snl_stats"))
os.chdir(script_path)
sys.path.append("..")


Affichage_pattern.affichage()

from interaction_stats.ml_stats import *
from interaction_stats.ml_stats_vizualisation import *
from interaction_stats.settings import *
from snl_stats.snl_stats_visualization import *


def page1():
    st.sidebar.markdown("Descriptive analysis")
    # #Barplots ______________________________________________________
    st.title('Descriptive analysis')
    st.header('Basic statistics on smiles and laughs')
    st.markdown("We look at the mean, median and standard deviation on the database.")
    st.subheader('By datasets')

    name_list=["Absolute duration", "Relative duration"]
    name_list_by_role=["absolute duration spk","absolute duration lsn","relative duration spk","relative duration lsn" ]
    expression_choice=st.radio("Expression choice ->", ['smiles', 'laughs','both'])
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    if expression_choice != 'both' :

        
        fig2 = plot_relative_duration(expression_choice)
        
        figs=st.selectbox(" Basic statistics plots : ", name_list) 
        
        if figs == 'Absolute duration' :

            choice_list=["Standard deviation", "Mean", "Median", "Max","Min","All"]
            choice=st.radio("Which feature do you want see ?  ->", choice_list)
            
            fig1 = plot_absolute_duration(expression_choice, choice)
            st.write(fig1)
        else :
            st.write(fig2)
    else : 

        kind =st.selectbox(" Basic statistics plots : ", name_list)

        if kind == 'Absolute duration' :
            choice_list=["Standard deviation", "Mean", "Median", "Max","Min","All"]
            choice=st.radio("Which feature do you want see ?  ->", choice_list)
            fig1_1, fig1_2 = plot_absolute_duration(expression_choice, choice)
            st.write(fig1_1, fig1_2)

        else : 
            fig2_1, fig2_2 = plot_relative_duration(expression_choice)
            st.write(fig2_1, fig2_2)

    st.subheader('By role')
    expression_choice=st.radio("Expression choice->", ['smiles', 'laughs', 'both'])
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    
    if expression_choice != 'both' :

        count = 0

        figs=st.selectbox(" Basic statistics plots by role - Absolute duration : ", name_list_by_role) 

        if "absolute" in figs :

            choice_list=["Standard deviation", "Mean", "Median", "Max","Min","All"]
            choice3= st.radio("Which feature do you want see ?  ->", choice_list, key = count)
            count += 1
            
            L= [plot_absolute_duration_from_spk(expression_choice, choice3), plot_absolute_duration_from_lsn(expression_choice, choice3)]

            for i in range(len(name_list_by_role)):
                if figs == name_list_by_role[i]:
                    st.write(L[i])
        
        else :

            L=[plot_relative_duration_from_spk(expression_choice), plot_relative_duration_from_lsn(expression_choice)]

            for i in range(len(name_list_by_role)):
                if figs == name_list_by_role[i]:
                    st.write(L[i])
   
    else : 

        count = 0
        figs=st.selectbox(" Basic statistics plots by role - Absolute duration : ", name_list_by_role) 
        fig1_1,fig1_2 = "",""

        if figs == "absolute duration spk" :

            choice_list=["Standard deviation", "Mean", "Median", "Max","Min","All"]
            choice1=st.radio("Which feature do you want see ?  ->", choice_list, key=count)
            count += 1
            fig1_1, fig1_2 = plot_absolute_duration_from_spk(expression_choice, choice1)
        
        elif figs == "absolute duration lsn" :

            choice_list=["Standard deviation", "Mean", "Median", "Max","Min","All"]
            choice2=st.radio("Which feature do you want see ?  ->", choice_list, key = count)
            count += 1
            fig1_1, fig1_2 = plot_absolute_duration_from_lsn(expression_choice, choice2)

        elif figs == "relative duration spk" :

            fig1_1, fig1_2 = plot_relative_duration_from_spk(expression_choice)
        
        elif figs == "relative duration lsn" :

            fig1_1, fig1_2 = plot_relative_duration_from_lsn(expression_choice)
        
        st.write(fig1_1, fig1_2)

page1()