import subprocess
import streamlit as st
import os, sys
import Affichage_pattern

Affichage_pattern.affichage()
script_path=os.path.realpath(os.path.dirname("src"))
os.chdir(script_path)
sys.path.append("..")

from src.page4.snl_stats_visualization_page4 import *
DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers=get_parameters()

def page3():
    st.sidebar.markdown("Non Verbal Expressions Effects")
    st.title('Effects analysis')
    st.markdown('''In this part, we want to know if an expression has an effect on another one.''')

    def page3_1():
        st.header('Intra Non Verbal Expressions Effects')

        st.subheader('Expressions Track')
        text_='''Here, we are checking what is before and after an expression in ploting percentage of the preceded and next expression.
        \n Track choice --> The expression we want to study.
        \n Check choice --> Expression before and after the track choice.
        '''
        st.markdown(text_)
        databases_name=[key.replace('_paths','').upper() for key in databases.keys()]
        expression_choices=list(tier_lists.keys())
        expression_choices_2=list(tier_lists.keys())
        track_choice=st.radio("Track choice: ", expression_choices, key='T1')
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        check_choice=st.radio("Check choice: ", expression_choices_2, key='C1')
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        # #st.subheader('Previous')
        fig1=plot_track_previous_expression(expression_track(check_choice, track_choice, DIR, databases_name), track_choice)
        fig2=plot_track_following_expression(expression_track(check_choice, track_choice, DIR, databases_name), track_choice)
        if fig1!=None:
            st.plotly_chart(fig1)
        else:
            st.write("No data to display")
        if fig2!=None: 
            st.plotly_chart(fig2)
        else:
            st.write("No data to display")

        st.subheader('Expressions Track By Entity')
        st.markdown("We do the same action as before but taking into account the entities of the expressions.")
        expression_choices1=list(tier_lists.keys())
        track_choice=st.radio("Track choice: ", expression_choices1, key='T2')
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        expression_choices2=list(tier_lists.keys())
        check_choice=st.radio("Check choice: ", expression_choices2, key='C2')
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        fig1= plot_track_previous_expression_byI(expression_track_byI(check_choice, track_choice, DIR, databases_name, tier_lists)[0], track_choice, check_choice)
        fig2= plot_track_following_expression_byI(expression_track_byI(check_choice, track_choice, DIR, databases_name, tier_lists)[1], track_choice, check_choice)
        if fig1!=None:
            st.plotly_chart(fig1)
        else:
            st.write("No data to display")
        if fig2!=None:
            st.plotly_chart(fig2) 
        else:
            st.write("No data to display")

    def page3_2():
        st.header('Inter Non Verbal Expressions Effects')

        st.subheader("Mimicry")
        st.markdown("We look at the capacity of someone to mimic someone else. ( A / B -> B mimic A)")
        name_database=[key.replace('_paths','').upper() for key in databases.keys()]
        databases_=[key for key in databases_pairs.keys()]
        databases_choice=st.selectbox("Datasets list: ", name_database)
        for i in range(len(databases_)):
            if databases_choice==databases_[i].replace('_pairs','').upper():
                databases_list=databases_pair_paths[databases_[i]]
        expression_choicesA=list(tier_lists.keys())
        expression_choicesB=list(tier_lists.keys())
        expression_choiceA=st.radio("Expression of person A:", expression_choicesA)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        expression_choiceB=st.radio("Mimicked expression by person B:", expression_choicesB)

        st.subheader(f'For {expression_choiceA} / {expression_choiceB}')
        if st.checkbox("All entities"):
            if tier_lists[expression_choiceA] and tier_lists[expression_choiceB]:
                fig=plot_mimicry(give_mimicry_folder2(databases_list, databases_choice.lower(), get_tier_dict_conv_folder, get_tier_dict_conv_folder, expression_choiceA, expression_choiceB))
                if fig!=None:
                    st.plotly_chart(fig)
                    st.text("Do you want to filter by another expression?")
                    filter_choice1=st.radio(label="  Choice: ", options=["Yes", "No"], key=1)
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                    if filter_choice1=="Yes":
                        expression_filter=list(tier_lists.keys())
                        expression_filter.remove(expression_choiceA)
                        if expression_choiceA!=expression_choiceB:
                            expression_filter.remove(expression_choiceB)
                        filter=st.multiselect("  Filter: ", expression_filter)
                        for i in filter:
                            for entity in tier_lists[i]:
                                try:
                                    fig=plot_mimicry(give_mimicry_folder3(databases_list, databases_choice.lower(), get_tier_from_tier, get_tier_from_tier, expression_choiceA, expression_choiceB, i, entity))
                                    if fig!=None:
                                        st.write(f"For {i} {entity}: ")
                                        st.plotly_chart(fig)
                                    else:
                                        st.write("No data to display")
                                except:
                                    st.write(f"No data to display for {entity} {i}")
                    else:
                        pass
                else: 
                    st.write("No data to display")
            else:
                st.write("No data to display")
        elif st.checkbox("By entity"): 
            st.write("For one particular entity: ")
            try:
                entities_A=st.radio(f"Entities for {expression_choiceA} of person A:", list(tier_lists[expression_choiceA]))
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                entities_B=st.radio(f"Entities for {expression_choiceB} of person B:", list(tier_lists[expression_choiceB]))   
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)   
                if entities_A and entities_B:
                    st.write(entities_B, f" {expression_choiceB} mimic ", entities_A, f" {expression_choiceA}: " )
                    fig=plot_mimicry(give_mimicry_folder2(databases_list, databases_choice.lower(), get_tier_dict_conv_folder, get_tier_dict_conv_folder, expression_choiceA, expression_choiceB, 'Intensity', 
                                        [str.lower(entities_A), str.lower(entities_B)]))
                    if fig!=None:
                        st.plotly_chart(fig)
                        st.text("Do you want to filter by another expression? ")
                        filter_choice2=st.radio(label="  Choice: ", options=["Yes", "No"] , key=2)
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                        if filter_choice2=="Yes":
                            expression_filter2=list(tier_lists.keys())
                            expression_filter2.remove(expression_choiceA)
                            if expression_choiceA!=expression_choiceB:
                                expression_filter2.remove(expression_choiceB)
                            filter=st.multiselect("  Filter: ", expression_filter2)
                            for i in filter:
                                for entity in tier_lists[i]:
                                    try:
                                        fig=plot_mimicry(give_mimicry_folder3(databases_list, databases_choice.lower(), get_tier_from_tier, get_tier_from_tier, expression_choiceA, expression_choiceB, i, entity, 'Intensity', [str.lower(entities_A), str.lower(entities_B)]))
                                        if fig!=None:
                                            st.write(f"For {i} {entity}: ")
                                            st.plotly_chart(fig)
                                        else:
                                            st.write("No data to display")
                                    except:
                                        st.write(f"No data to display for {entity} {i}")
                        else:
                            pass
                    else:
                        st.write("No data to display")
                else:
                    st.write("No data to display")
            except:
                return None

    def page3_3():               
        st.header('Correlation')
        st.markdown('''Here, we look at the correlation between two sequences of expressions.
                    \nBe careful if the selected sampling values (shift and width) are too large or not adequate, you may have zero correlation graphs. 
                    \n\nYou must select appropriate values according to the annotation times of your files.''')

        st.subheader("********    By dataset    ********")
        name_databases=[key.replace('_paths','').upper() for key in databases.keys()]
        databases_=[key for key in databases_pairs.keys()]
        databases_choice=st.selectbox("Datasets list: ", name_databases, key = '0')
        for i in range(len(databases_)):
            if databases_choice==databases_[i].replace('_pairs','').upper():
                databases_list=databases_pair_paths[databases_[i]]
        case_=st.radio("Cases: ", [1, 2])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        expression_choicesA=list(tier_lists.keys())
        expression_choicesB=list(tier_lists.keys())
        if case_==1: 
            A_choice=st.radio("Expression ->", expression_choicesA)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            if tier_lists[A_choice]:
                width=st.slider("Select the width: ", 1, 344, key='W1') 
                shift=st.slider("Select the shift: ", 1, 344, key='S1') 
                fig=plot_correlation(get_correlation_folder(A_choice, databases_list, width, shift), databases_list)
                if fig!=None:
                    st.plotly_chart(fig)
                else:
                    st.write("No data to display")
            else:
                st.write("No data to display")
        else:
            A_choice=st.radio("Expression A ->", expression_choicesA)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            B_choice=st.radio("Expression B ->", expression_choicesB)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            if tier_lists[A_choice] and tier_lists[B_choice]:     
                width=st.slider("Select the width: ", 1, 344, key='W2') 
                shift=st.slider("Select the shift: ", 1, 344, key='S2') 
                fig=plot_correlation(get_correlation_folder(A_choice, databases_list, width, shift, B_choice), databases_list)
                if fig!=None:
                    st.plotly_chart(fig)
                else:
                    st.write("No data to display")
            else:
                st.write("No data to display")

        st.subheader("********    By dataset and expression    ********")
        name_databases1=[key.replace('_paths','').upper() for key in databases.keys()]
        databases_1=[key for key in databases_pairs.keys()]
        databases_choice1=st.selectbox("Datasets list: ", name_databases1, key='1')
        for i in range(len(databases_1)):
            if databases_choice1==databases_1[i].replace('_pairs','').upper():
                databases_list1=databases_pair_paths[databases_1[i]]

        st.markdown("Between two expressions or two entities")
        st.text("EXPLICATION:")
        st.markdown("--> Choose if you want to look at the correlation between two different expressions (2) or not (1).")
        case_=st.radio("Cases expressions: ", [1, 2])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        expression_choicesA=list(tier_lists.keys())
        expression_choicesB=list(tier_lists.keys()) 
        if case_==1:
            A_choice=st.radio("Expression: ", expression_choicesA)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            width=st.slider("Select the width: ", 1, 344, key='W3')
            shift=st.slider("Select the shift: ", 1, 344, key='S3')
            if tier_lists[A_choice]:
                case_level=st.radio("Cases entities: ", [1, 2])
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                entity_levelA=tier_lists[A_choice]
                if case_level==1:
                    entity1=st.radio("Entity 1: ", entity_levelA)
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                    fig=plot_correlation(get_correlation_byI(A_choice, entity1, databases_list1, width, shift), databases_list1)
                    if fig!=None:
                        st.plotly_chart(fig)  
                    else:
                        st.write("No data to display")
                else:
                    entity1=st.radio("Entity 1: ", entity_levelA)
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                    entity2=st.radio("Entity 2: ", entity_levelA)
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                    fig=plot_correlation(get_correlation_byI(A_choice, entity1, databases_list1, width, shift, entity2=entity2), databases_list1)
                    if fig!=None:
                        st.plotly_chart(fig)
                    else:
                        st.write("No data to display")
            else:
                st.write("No data to display")
        else:
            A_choice=st.radio("Expression A:", expression_choicesA)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            B_choice=st.radio("Expression B:", expression_choicesB)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            width=st.slider("Select the width: ", 1, 344, key='W4') 
            shift=st.slider("Select the shift: ", 1, 344, key='S4')
            if tier_lists[A_choice] and tier_lists[B_choice]:
                case_level=st.radio("Cases entities: ", [1, 2])
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                entity_levelA=tier_lists[A_choice]
                entity_levelB=tier_lists[B_choice]
                if case_level==1:
                    entity1 = st.radio("Entity 1: ", entity_levelA)
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                    fig=plot_correlation(get_correlation_byI(A_choice, entity1, databases_list1, width, shift, B_choice), databases_list1)
                    if fig!=None:
                        st.plotly_chart(fig)
                    else:
                        st.write("No data to display")
                else:
                    entity1=st.radio("Entity 1: ", entity_levelA)
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                    entity2=st.radio("Entity 2: ", entity_levelB)
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                    fig=plot_correlation(get_correlation_byI(A_choice, entity1, databases_list1, width, shift, B_choice, entity2), databases_list1)
                    if fig!=None:
                        st.plotly_chart(fig)
                    else:
                        st.write("No data to display")
            else:
                st.write("No data to display")
        

    page3_names_to_funcs={
        "Intra Non Verbal Expressions Effects": page3_1,
        "Inter Non Verbal Expressions Effects": page3_2,
        "Correlation": page3_3,
    }

    selected_page=st.sidebar.selectbox("Select a page", page3_names_to_funcs.keys())
    page3_names_to_funcs[selected_page]()

subprocess.run(["python", "..\\src\\snl_stats_extraction_data.py"])
page3()