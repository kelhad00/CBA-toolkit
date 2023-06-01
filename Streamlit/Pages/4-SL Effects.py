import subprocess
import streamlit as st
import os, sys, json
import Affichage_pattern
script_path = os.path.realpath(os.path.dirname("src"))
os.chdir(script_path)
sys.path.append("..")


Affichage_pattern.affichage()

# from interaction_stats.ml_stats import *
# from interaction_stats.ml_stats_vizualisation import *
# from interaction_stats.settings import *
from src.page4.snl_stats_visualization_page4 import *

DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()

def page3():
    st.sidebar.markdown("Non Verbal Expressions Effects")
    st.title('Effects analysis')
    st.markdown('''In this part, we want to know if an expression has an effect on another one.''')

    def page3_1():
        st.header('Intra Non Verbal Expressions Effects')
        st.subheader('Expressions Track')
        text_='''Here, we are checking what is before and after an expression in ploting percentage of the preceded and next expression.
        \n Track choice --> The expression we want to study
        \n Check choice --> Expression before and after the track choice.
        '''
        st.markdown(text_)
        databases_name = [key.split('_')[0].upper() for key in databases.keys()]
        expression_choices = list(tier_lists.keys())
        expression_choices_2 = list(tier_lists.keys())
        track_choice=st.radio("Track choice: ", expression_choices)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        check_choice=st.radio("Check choice: ", expression_choices_2)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        # #st.subheader('Previous')
        fig1= plot_track_previous_expression(expression_track(check_choice, track_choice, DIR, databases_name), track_choice)
        fig2= plot_track_following_expression(expression_track(check_choice, track_choice, DIR, databases_name), track_choice)
        if fig1 != None :
            st.plotly_chart(fig1)
        else:
            st.write("No data to display")
        if fig2 != None : 
            st.plotly_chart(fig2)
        else:
            st.write("No data to display")

        st.subheader('Expressions Track by intensity')
        st.markdown("We do the same action as before but taking into account the intensities.")
        expression_choices1 = list(tier_lists.keys())
        track_choice=st.radio("Track choice:", expression_choices1)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        expression_choices2 = list(tier_lists.keys())
        check_choice=st.radio("Check choice:", expression_choices2)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        fig1= plot_track_previous_expression_byI(expression_track_byI(check_choice, track_choice, DIR, databases_name, tier_lists)[0], track_choice, check_choice)
        fig2= plot_track_following_expression_byI(expression_track_byI(check_choice, track_choice, DIR, databases_name, tier_lists)[1], track_choice, check_choice)
        if fig1 != None :
            st.plotly_chart(fig1)
        else:
            st.write("No data to display")
        if fig2 != None :
            st.plotly_chart(fig2) 
        else:
            st.write("No data to display")

    def page3_2():
        st.header('Inter S&L effects')
        st.subheader("Mimicry")
        st.markdown("We look at the capacity of someone to mimic someone else. ( A / B -> B mimic A)")
        name_database = [key.rstrip('_paths').upper() for key in databases.keys()]
        databases_=[key for key in databases_pairs.keys()]
        databases_choice=st.selectbox("Databases list:", name_database)
        for i in range(len(databases_)):
            if databases_choice==databases_[i].rstrip('_pairs').upper():
                databases_list=databases_pair_paths[databases_[i]]
        expression_choicesA = list(tier_lists.keys())
        expression_choicesB = list(tier_lists.keys())
        expression_choiceA=st.radio("Expression of person A:", expression_choicesA)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        expression_choiceB=st.radio("Mimicked expression by person B:", expression_choicesB)

        st.subheader(f'For {expression_choiceA} / {expression_choiceB}')
        if st.checkbox("All entities"):
            if tier_lists[expression_choiceA] and tier_lists[expression_choiceB]:
                fig=plot_mimicry(give_mimicry_folder2(databases_list, databases_choice.lower(), get_tier_dict_conv_folder, get_tier_dict_conv_folder, expression_choiceA, expression_choiceB))
                if fig != None :
                    st.plotly_chart(fig)
                    st.text("Do you want to filter by another expression?")
                    filter_choice=st.radio(label="  Choice:", options=["Yes", "No"])
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                    if filter_choice == "Yes":
                        expression_filter = list(tier_lists.keys())
                        expression_filter.remove(expression_choiceA)
                        if expression_choiceA != expression_choiceB:
                            expression_filter.remove(expression_choiceB)
                        filter=st.multiselect("  Filter:", expression_filter)
                        for i in filter :
                            for entity in tier_lists[i]:
                                # fig=plot_mimicry(give_mimicry_folder2(databases_choice, databases_, eval('get_smiles_from_'+i+'_folder'), eval('get_laughs_from_'+i+'_folder')))
                                fig=plot_mimicry(give_mimicry_folder3(databases_list, databases_choice.lower(), get_tier_from_tier, get_tier_from_tier, expression_choiceA, expression_choiceB, i, entity))
                                if fig != None:
                                    st.write(f"For {i} {entity}:")
                                    st.plotly_chart(fig)
                                else :
                                    st.write("No data to display")
                    else:
                        pass
                else : 
                    st.write("No data to display")
            else:
                st.write("No data to display")
        if st.checkbox("By entity"): 
            st.write("For one particular entity : ")
            try :
                intensities_A = st.radio(f"Entities for {expression_choiceA} of person A:", list(tier_lists[expression_choiceA]))
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                intensities_B = st.radio(f"Entities for {expression_choiceB} of person B:", list(tier_lists[expression_choiceB]))   
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)   
                if intensities_A and intensities_B:
                    st.write(intensities_B, f" {expression_choiceB} mimic ", intensities_A, f" {expression_choiceA}: " )
                    fig = plot_mimicry(give_mimicry_folder2(databases_list, databases_choice.lower(), get_tier_dict_conv_folder, get_tier_dict_conv_folder, expression_choiceA, expression_choiceB, 'Intensity', 
                                        [str.lower(intensities_A), str.lower(intensities_B)] ))
                    if fig != None:
                        st.plotly_chart(fig)
                        st.text("Do you want to filter by another expression?")
                        filter_choice=st.radio(label="Choice ->", options=["Yes", "No"])
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                        if filter_choice == "Yes":
                            expression_filter = list(tier_lists.keys())
                            expression_filter.remove(expression_choiceA)
                            if expression_choiceA != expression_choiceB:
                                expression_filter.remove(expression_choiceB)
                            filter=st.multiselect(" Filter:", expression_filter)
                            for i in filter :
                                for entity in tier_lists[i]:
                                    fig=plot_mimicry(give_mimicry_folder3(databases_list, databases_choice.lower(), get_tier_from_tier, get_tier_from_tier, expression_choiceA, expression_choiceB, i, entity, 'Intensity', [str.lower(intensities_A), str.lower(intensities_B)]))
                                    if fig != None:
                                        st.write(f"For {i} {entity}:")
                                        st.plotly_chart(fig)
                                    else :
                                        st.write("No data to display")
                        else:
                            pass
                    else :
                        st.write("No data to display")
                else :
                    st.write("No data to display")
            except :
                return None

        

    def page3_3():               
        st.header('Correlation')
        st.markdown('Here, we look at the correlation between two sequences of expressions')
        st.text(" *******  By dataset  ********")

        name_databases=['CCDB','IFADV','NDC']
        databases_=[databases_pair_paths["ccdb_pairs"], databases_pair_paths["ifadv_pairs"], databases_pair_paths["ndc_pairs"]]
        databases_choice=st.selectbox("Databases list :", name_databases)
        for i in range(len(name_databases)):
            if databases_choice==name_databases[i]:
                databases_choice=databases_[i]

        case_SL= st.radio("Cases S&L:", [1, 2])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        if case_SL==1:
            A_choice=st.radio("Expression A ->", ['S', 'L'])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            width = st.slider("Select the width", 1, 344) 
            shift = st.slider("Select the shift", 1, 344) 
            st.write(plot_correlation(get_correlation_folder(A_choice,databases_choice,width,shift)))
        else:
            A_choice=st.radio("Expression A->", ['S', 'L'])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            B_choice=st.radio("Expression B ->", ['S', 'L'])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            width = st.slider(" Select the width ", 1, 344) 
            shift = st.slider(" Select the shift ", 1, 344) 
            st.write(plot_correlation(get_correlation_folder(A_choice,databases_choice,width,shift,B_choice)))


        st.text("********    By dataset and expression   ********")
        databases_=[databases_pair_paths["ccdb_pairs"], databases_pair_paths["ifadv_pairs"], databases_pair_paths["ndc_pairs"]]
        databases_choice=st.selectbox("Databases list --> ", name_databases)
        for i in range(len(name_databases)):
            if databases_choice==name_databases[i]:
                databases_choice=databases_[i]

        st.text("Between two expressions or two intensities")
        st.text("EXPLICATION")
        st.text("Choose if you want to look at the correlation between two different expressions (2) or not (1).")
        case_SL= st.radio("Cases S&L : ", [1, 2])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        width = st.slider("Select the width ", 1, 340) 
        shift = st.slider("Select the shift ", 1, 340) 
        if case_SL==1 :
            A_choice=st.radio("Expression -> ", ['Smiles', 'Laughs'])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            
            case_level= st.radio("Cases intensities: ", [1, 2])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            
            if case_level==1:
                intensity1 = st.multiselect("Intensity 1:", ["subtle", "low", "medium", "high"])

                st.write(plot_correlation(get_correlation_byI(A_choice,intensity1,databases_choice,width,shift)))
            else:
                intensity1 = st.multiselect("Intensity 1 :", ["subtle", "low", "medium", "high"])
                intensity2 = st.multiselect("Intensity 2 :", ["subtle", "low", "medium", "high"])
         
                st.write(plot_correlation(get_correlation_byI(A_choice,intensity1,databases_choice,width,shift, SL2=None,intensity2=intensity2)))
        else:
            A_choice=st.radio("Expression A -> ", ['Smiles', 'Laughs'])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            B_choice=st.radio("Expression B -> ", ['Smiles', 'Laughs'])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            
            case_level= st.radio("Cases intensities : ", [1, 2])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            
            if case_level==1:
                intensity1 = st.multiselect("Intensity 1 ->", ["subtle", "low", "medium", "high"])

                st.write(plot_correlation(get_correlation_byI(A_choice,intensity1,databases_choice,width,shift, B_choice)))
            else:
                intensity1 = st.multiselect("Intensity 1 -> ", ["subtle", "low", "medium", "high"])
                intensity2 = st.multiselect("Intensity 2 -> ", ["subtle", "low", "medium", "high"])

                st.write(plot_correlation(get_correlation_byI(A_choice,intensity1,databases_choice,width,shift, B_choice, intensity2)))

        

    page3_names_to_funcs = {
        "Intra S&L effects": page3_1,
        "Inter S&L effects": page3_2,
        "Correlation": page3_3,
    }

    selected_page = st.sidebar.selectbox("Select a page", page3_names_to_funcs.keys())
    page3_names_to_funcs[selected_page]()

subprocess.run(["python", "..\\src\\snl_stats_extraction_data.py"])
page3()