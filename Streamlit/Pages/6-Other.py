import subprocess
import streamlit as st
import os, sys, json
import Affichage_pattern 
import threading

script_path = os.path.realpath(os.path.dirname("src"))
os.chdir(script_path)
sys.path.append("..")

Affichage_pattern.affichage()

# from interaction_stats.ml_stats import *
# from interaction_stats.ml_stats_vizualisation import *
# from interaction_stats.settings import *
from src.page6.snl_stats_visualization_page6 import *
from src.page6.snl_stats_visualisation_database import *

DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()

def page5():
    st.markdown("Here, we explore other areas to describe and see what we have in our database. \nLet's see each page !")
    
    def page5_1():
        st.sidebar.markdown("Expression per minute", )
        # # #Barplots ______________________________________________________
        st.header('Expression per minute')
        st.markdown("We count the number of tiers we have in one minute in each dataset.")
        name_databases = [key.rstrip('_paths').upper() for key in databases.keys()]
        databases_ = [value for value in databases_pair_paths.values()]
        databases_choice=st.selectbox("Datasets list :", name_databases)
        for i in range(len(name_databases)):
            if databases_choice==name_databases[i]:
                databases_choice=databases_[i]

        if st.checkbox("All intensities"):
            expression_choice=st.radio("Expression:", list(tier_lists.keys()))
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

            expression_choice = expression_choice
            choices_case=["Intra","Inter"]
            case_choice = st.radio("Case:", choices_case)
            case_list=[None, 2]
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            for _ in range (len(case_list)):
                if case_choice==choices_case[_]:
                    case_choice=case_list[_]
            if(plot_expression_per_min(databases_choice, expression_choice, case_choice) == None):

                st.write("No data available")
            
            else :

                st.plotly_chart(plot_expression_per_min(databases_choice, expression_choice, case_choice))

        if st.checkbox("By intensity"):
            expression_choice=st.radio("Expression: ", list(tier_lists.keys()))
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

            intensity_choice= st.radio("Intensity: ", tier_lists[expression_choice])
            if intensity_choice is not None:
                if (plot_expression_per_min_I(databases_choice, expression_choice, str.lower(intensity_choice) == None)) :
                    str.write("No data available")
                else :
                    st.plotly_chart(plot_expression_per_min_I(databases_choice, expression_choice, str.lower(intensity_choice)))
            else :
                st.write("No data available")

    def page5_2() :

        st.sidebar.markdown("Database Information", )
        st.header('Database Information')
        name_databases = [key.rstrip('_paths').upper() for key in databases.keys()]
        databases_ = [value for value in databases_pair_paths.values()]
        databases_choice=st.selectbox("Datasets list:", name_databases)
        name_tiers = list(tier_lists.keys()) + ["GENERAL"]
        tiers_choice=st.selectbox("Tiers list:", name_tiers, index=name_tiers.index("GENERAL"))

        for i in range(len(name_databases)):
            if databases_choice==name_databases[i]:
                databases_choice=databases_[i]
        if tiers_choice == 'GENERAL' :
            data = display_general_informations_files(databases_choice)
            columns_names = ["Filename", "Duration"] + list(tier_lists.keys())
            df = pd.DataFrame(data, columns=columns_names)
            st.table(df)
        
        else :
            data = display_specific_informations(databases_choice, tiers_choice, tier_lists.get(tiers_choice))
            columns_names = ["Filename", "Max duration", "Min duration"] +  tier_lists.get(tiers_choice)
            df = pd.DataFrame(data, columns=columns_names)
            st.write(df)

    
    page5_names_to_funcs = {
        "Expression per minute": page5_1,
        "Database Information": page5_2,
    }

    selected_page = st.sidebar.selectbox("Select a page", page5_names_to_funcs.keys())
    page5_names_to_funcs[selected_page]()

subprocess.run(["python", "..\\src\\snl_stats_extraction_data.py"])
page5()