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
from src.page5.snl_stats_visualization_page5 import *



def page5():
    st.markdown("Here, we explore other areas to describe and see what we have in our database. \nLet's see each page !")
    
    def page5_1():
        st.sidebar.markdown("Expression per minute")
        # # #Barplots ______________________________________________________
        st.title('Expression per minute')
        st.markdown("We count the number of smiles or laughs we have in one minute in each dataset.")
        name_databases = [key.split('_')[0].upper() for key in databases.keys()]
        databases_ = [value for value in databases_pair_paths.values()]
        databases_choice=st.selectbox("Datasets list :", name_databases)
        for i in range(len(name_databases)):
            if databases_choice==name_databases[i]:
                databases_choice=databases_[i]

        if st.checkbox("All intensities"):
            expression_choice=st.radio("Expression :", list(tier_lists.keys()))
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

            # if expression_choice=='Smiles':
            #     expression_choice='Smiles_0'
            # else:
            #     expression_choice='Laughs_0'
            expression_choice = expression_choice + '_0'
            choices_case=["Intra","Inter"]
            case_choice = st.radio("Case :", choices_case)
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
            expression_choice=st.radio("Expression : ", list(tier_lists.keys()))
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

            intensity_choice= st.radio("Intensity : ", tier_lists[expression_choice])
            try :
                if (plot_expression_per_min_I(databases_choice, expression_choice, str.lower(intensity_choice) == None)) :
                    str.write("No data available ")
                else :
                    st.plotly_chart(plot_expression_per_min_I(databases_choice, expression_choice, str.lower(intensity_choice)))
            except :

                try :

                    if (plot_expression_per_min_I(databases_choice, expression_choice, intensity_choice == None)) :
                        str.write("No data available")
                    else :
                        st.plotly_chart(plot_expression_per_min_I(databases_choice, expression_choice, intensity_choice))
                
                except :

                    st.write("No data available")

    page5_names_to_funcs = {
        "Expression per minute": page5_1,
    }

    selected_page = st.sidebar.selectbox("Select a page", page5_names_to_funcs.keys())
    page5_names_to_funcs[selected_page]()

page5()