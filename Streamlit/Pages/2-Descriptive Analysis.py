import streamlit as st
import os, sys, json
from fuzzywuzzy import fuzz
import Affichage_pattern
script_path = os.path.realpath(os.path.dirname("src"))
os.chdir(script_path)
sys.path.append("..")


Affichage_pattern.affichage()

# from interaction_stats.ml_stats import *
# from interaction_stats.ml_stats_vizualisation import *
# from interaction_stats.settings import *
from src.page2.snl_stats_visualization_page2 import *


def page1():
    st.sidebar.markdown("Descriptive analysis")
    # #Barplots ______________________________________________________
    st.title('Descriptive analysis')
    st.header('Basic statistics on smiles and laughs')
    st.markdown("We look at the maximum, minimum, mean, median and standard deviation on the database.")

    st.subheader('By datasets')

    name_list=["Absolute duration", "Relative duration"]
    expression_choices = list(tier_lists.keys())
    expression_choices.append('all')
    expression_choice=st.radio("Expression choice :", expression_choices)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    name_databases = [key.split('_')[0].upper() for key in databases.keys()]
    figs=st.selectbox(" Basic statistics plots : ", name_list) 
    choice_list=["Standard deviation", "Mean", "Median", "Max", "Min", "All"]
    choice=st.radio("Which feature do you want see ?  ", choice_list)

    if expression_choice != 'all' :
        if figs == 'Absolute duration' :
            fig1_0 = plot_absolute_duration(expression_choice, choice, name_databases)
            if fig1_0 != None :    
                st.write(fig1_0)
            else :
                st.write("No Data available")
        else :
            fig2_0 = plot_relative_duration(expression_choice, choice, name_databases)
            if fig2_0 != None :
                st.write(fig2_0)
            else :
                st.write("No Data available")
            
    elif expression_choice == 'all' : 
        figures1 = []
        if figs == 'Absolute duration' :
            fig1_1 = plot_absolute_duration(expression_choice, choice, name_databases)
            figures1.extend(fig1_1)

        else : 
            fig2_1 = plot_relative_duration(expression_choice, choice, name_databases)
            figures1.extend(fig2_1)

        for fig in figures1:
            if fig != None :
                st.write(fig)
            else :
                st.write("No Data available")

    st.subheader('Basic statistics plots :')  # By role : 

    expression_choices_1 = expression_choices.copy()
    expression_choices_1.remove('all')
    expression_choice_1=st.radio("By : ", expression_choices_1)
    expression_values = tier_lists[expression_choice_1]
    if expression_values :
        name_list_by_expression_kind1 = [f"Absolute duration from {expression_choice_1.lower()}" ]
        name_list_by_expression_kind2 = [f"Relative duration from {expression_choice_1.lower()}"]
        name_list_by_expression = name_list_by_expression_kind1 + name_list_by_expression_kind2
        
        expression_choices_copy = expression_choices.copy()
        expression_choices_copy.remove(expression_choice_1) # role_tier_name
        expression_choice_copy=st.radio("Expression choice : ", expression_choices_copy)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        count = 0
        figs1=st.selectbox(" Basic statistics plots by role : ", name_list_by_expression) # name_list_by_role
        choice_list1=["Standard deviation", "Mean", "Median", "Max", "Min", "All"]
        choice1= st.radio("Which feature do you want see ?  ", choice_list1, key = count)
        if expression_choice_copy != 'all' :
            if "Absolute" in figs1 :
                count += 1
                for entity in expression_values :
                    fig1_temp = plot_absolute_duration_from_tier(expression_choice_1, entity, expression_choice_copy, choice1, name_databases)
                    if fig1_temp != None :
                        st.write(fig1_temp)    
                    else :
                        st.write("No Data available")

            elif "Relative" in figs1 :
                count += 1
                for entity in expression_values :
                    fig1_temp = plot_relative_duration_from_tier(expression_choice_1, entity, expression_choice_copy, choice1, name_databases)
                    if fig1_temp != None :
                        st.write(fig1_temp)
                    else : 
                        st.write("No Data available")
   
        elif expression_choice_copy == 'all' : 
            figures = []

            if "Absolute" in figs1 :
                count += 1
                for entity in expression_values :
                    fig1_temp = plot_absolute_duration_from_tier(expression_choice_1, entity, expression_choice_copy, choice1, name_databases)
                    figures.extend(fig1_temp)

            elif "Relative" in figs1 :
                count += 1
                for entity in expression_values :
                    fig1_temp = plot_relative_duration_from_tier(expression_choice_1, entity, expression_choice_copy, choice1, name_databases)
                    figures.extend(fig1_temp)
            
            for fig_R in figures : 
                if fig_R != None :
                    st.write(fig_R)
                else :
                    st.write("No Data available")
    else :
        st.write("No data available")


page1()