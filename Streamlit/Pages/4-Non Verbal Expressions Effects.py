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

real_tier_lists , real_tiers = get_parameters_tag()

def page3():
    st.sidebar.markdown("Non Verbal Expressions Effects")
    st.title('Effects analysis')
    st.markdown('''In this part, we want to know if an expression has an effect on another one.''')
    st.markdown(''' ''')
    st.markdown(''' ''')

    def page3_1():
        st.header('Intra Non Verbal Expressions Effects')
        st.subheader('Expressions Track')
        st.markdown('''Here, we are checking what is before and after an expression in ploting percentage of the preceded and next expression for each individual. 
        \nThat's mean we look at the sequence of expressions of an individual in order to see if there is any pattern or influence of the expressions in a same sequence.''')
        st.markdown('''Explanations of the choices:''')
        st.write("<style>body { font-size: 14px; }</style><i>Track choice --> The expression we want to study.</i>", unsafe_allow_html=True)
        st.write("<style>body { font-size: 14px; }</style><i>Check choice --> Expression before and after the track choice.</i>", unsafe_allow_html=True)
        st.markdown(''' ''')
        databases_name=[key.replace('_paths','').upper() for key in databases.keys()]
        expression_choices=list(real_tier_lists.keys())
        expression_choices_2=list(real_tier_lists.keys())
        track_choice=st.radio("Track choice: ", expression_choices, key='T1')
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        check_choice=st.radio("Check choice: ", expression_choices_2, key='C1')
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
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
        st.markdown(''' ''')
        st.markdown('''---------------------------------------------------------------------------------------------''')
        st.markdown(''' ''')
        st.subheader('Expressions Track By Entity')
        st.markdown("We do the same action as before but taking into account the entities of the expressions.")
        expression_choices1=list(real_tier_lists.keys())
        track_choice=st.radio("Track choice: ", expression_choices1, key='T2')
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        expression_choices2=list(real_tier_lists.keys())
        check_choice=st.radio("Check choice: ", expression_choices2, key='C2')
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        fig1= plot_track_previous_expression_byI(expression_track_byI(check_choice, track_choice, DIR, databases_name, real_tier_lists)[0], track_choice, check_choice)
        fig2= plot_track_following_expression_byI(expression_track_byI(check_choice, track_choice, DIR, databases_name, real_tier_lists)[1], track_choice, check_choice)
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
        st.markdown('''We look at the capacity of someone to mimic someone else expression in an interaction. 
                    /nA / B -> person B mimic person A.
                    /nB / A -> person A mimic person B.''')
        mimic_choices=['A/B', 'B/A']
        mimic_choice=st.radio("Do you want to study all B files mimicking A files or the opposite ? ", mimic_choices)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        name_database=[key.replace('_paths','').upper() for key in databases.keys()]
        databases_=[key for key in databases_pairs.keys()]
        databases_choice=st.selectbox("Dataset choice: ", name_database)
        for i in range(len(databases_)):
            if databases_choice==databases_[i].replace('_pairs','').upper():
                databases_list=databases_pair_paths[databases_[i]]
        expression_choicesA=list(real_tier_lists.keys())
        expression_choicesB=list(real_tier_lists.keys())
        expression_choiceA=st.radio("Expression of person A:", expression_choicesA)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        expression_choiceB=st.radio("Mimicked expression by person B:", expression_choicesB)

        st.subheader(f'For {expression_choiceA} / {expression_choiceB}')
        if st.checkbox("All entities"):
            if real_tier_lists[expression_choiceA] and real_tier_lists[expression_choiceB]:
                delta = st.number_input('Delta time in ms (Time after which expression occuring still counts as mimicry):', min_value=0, step=1)
                max_eaf_durations = get_time_eaf(databases_list, tiers=None)
                max_duration = min(max_eaf_durations) * 1000
                if delta>max_duration:
                    st.error(f"The delta time exceeds the duration of the EAF files, please choose a lower value (max: {max_duration} ms)")
                else:
                    try:
                        fig=plot_mimicry(give_mimicry_folder2(databases_list, databases_choice.lower(), get_tier_dict_conv_folder, get_tier_dict_conv_folder, expression_choiceA, expression_choiceB, delta_t=delta, mimic_choice=mimic_choice))
                        if fig!=None:
                            st.plotly_chart(fig)
                            st.text("Do you want to divide/filter by another expression?")
                            filter_choice1=st.radio(label="  Choice: ", options=["Yes", "No"], key=1)
                            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                            if filter_choice1=="Yes":
                                expression_filter=list(tier_lists.keys())
                                expression_filter.remove(expression_choiceA)
                                if expression_choiceA!=expression_choiceB:
                                    expression_filter.remove(expression_choiceB)
                                filter=st.multiselect("  Filter: ", expression_filter)
                                for i in filter:
                                    entities1 = tier_lists[i]
                                    entities2 = tier_lists[i]
                                    entity1 = st.radio(f"  Entity of {i} for person A:", entities1)
                                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                                    entity2 = st.radio(f"  Entity of {i} for person B:", entities2)
                                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                                    if entity1 and entity2:
                                        try:
                                            fig=plot_mimicry(give_mimicry_folder4(databases_list, databases_choice.lower(), get_tier_from_tier, get_tier_from_tier, expression_choiceA, expression_choiceB, tier_filter=i, entity1=entity1, entity2=entity2, delta_t=delta, mimic_choice=mimic_choice))
                                            if fig!=None:
                                                st.write(f"For {entity2} mimicking {entity1} - {i}: ")
                                                st.plotly_chart(fig)
                                            else:
                                                st.write("No data to display")
                                        except:
                                            st.write(f"No data to display for {entity2} mimicking {entity1} - {i}")
                            else:
                                pass
                        else: 
                            st.write("No data to display")
                    except:
                        st.write("The delta time is too high, please choose a lower value.")
            else:
                st.write("No data to display")
        elif st.checkbox("By entity"): 
            st.write("For one particular entity: ")
            try:
                if real_tier_lists[expression_choiceA]['Replace_Value'] != "" :
                    entities_A = st.radio(f"Entities for {expression_choiceA} of person A:", [real_tier_lists[expression_choiceA]['Replace_Value'], str("No_" + real_tier_lists[expression_choiceA]['Replace_Value'])])
                else :
                    entities_A=st.radio(f"Entities for {expression_choiceA} of person A:", list(real_tier_lists[expression_choiceA]['Intensities']))
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True) 
                if real_tier_lists[expression_choiceB]['Replace_Value'] != "" :
                    entities_B = st.radio(f"Entities for {expression_choiceB} of person B:", [real_tier_lists[expression_choiceB]['Replace_Value'], str("No_" + real_tier_lists[expression_choiceB]['Replace_Value'])])
                else :
                    entities_B=st.radio(f"Entities for {expression_choiceB} of person B:", list(real_tier_lists[expression_choiceB]['Intensities']))
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)   
                if entities_A and entities_B:
                    delta = st.number_input('Delta time in ms (Time after which expression occuring still counts as mimicry):', min_value=0, step=1)
                    max_eaf_durations = get_time_eaf(databases_list, tiers=None)
                    max_duration = min(max_eaf_durations) * 1000
                    if delta>max_duration:
                        st.error(f"The delta time exceeds the duration of the EAF files, please choose a lower value (max: {max_duration} ms)")
                    else:   
                        try:
                            st.write(entities_B, f" {expression_choiceB} mimic ", entities_A, f" {expression_choiceA}: " )
                            fig=plot_mimicry(give_mimicry_folder2(databases_list, databases_choice.lower(), get_tier_dict_conv_folder, get_tier_dict_conv_folder, expression_choiceA, expression_choiceB, 'Intensity', 
                                                [entities_A, entities_B], delta_t=delta, mimic_choice=mimic_choice))
                            if fig!=None:
                                st.plotly_chart(fig)
                                st.text("Do you want to divide/filter by another expression? ")
                                filter_choice2=st.radio(label="  Choice: ", options=["Yes", "No"] , key=2)
                                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                                if filter_choice2=="Yes":
                                    expression_filter2=list(tier_lists.keys())
                                    expression_filter2.remove(expression_choiceA)
                                    if expression_choiceA!=expression_choiceB:
                                        expression_filter2.remove(expression_choiceB)
                                    filter=st.multiselect("  Filter: ", expression_filter2)
                                    for i in filter:
                                        entities1 = tier_lists[i]
                                        entities2 = tier_lists[i]
                                        entity1 = st.radio(f"  Entity of {i} for person A:", entities1)
                                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                                        entity2 = st.radio(f"  Entity of {i} for person B:", entities2)
                                        if entity1 and entity2:
                                            try:
                                                fig=plot_mimicry(give_mimicry_folder4(databases_list, databases_choice.lower(), get_tier_from_tier, get_tier_from_tier, expression_choiceA, expression_choiceB, tier_filter=i, entity1=entity1, entity2=entity2, filter='Intensity', label=[str.lower(entities_A), str.lower(entities_B)], delta_t=delta, mimic_choice=mimic_choice))
                                                if fig!=None:
                                                    st.write(f"For {entity2} mimicking {entity1} - {i}: ")
                                                    st.plotly_chart(fig)
                                                else:
                                                    st.write("No data to display")
                                            except:
                                                st.write(f"No data to display for {entity2} mimicking {entity1} - {i}")
                                else:
                                    pass
                            else:
                                st.write("No data to display")
                        except:
                            st.write("The delta time is too high, please choose a lower value.")
                else:
                    st.write("No data to display")
            except:
                return None

    def page3_3():               
        st.header('Correlation')
        key = 1
        st.markdown('''Here, we look at the correlation between two sequences of expressions.
                    \nBe careful if the selected sampling values (shift and width) are too large or not adequate, you may have zero correlation graphs. 
                    \n\nYou must select appropriate values according to the annotation times of your files.''')
        st.markdown(''' ''')
        st.subheader("********    By dataset    ********")
        name_databases=[key.replace('_paths','').upper() for key in databases.keys()]
        databases_=[key for key in databases_pairs.keys()]
        databases_choice=st.selectbox("Dataset choice: ", name_databases, key = '0')
        for i in range(len(databases_)):
            if databases_choice==databases_[i].replace('_pairs','').upper():
                databases_list=databases_pair_paths[databases_[i]]
        case_=st.radio("Choose whether you want to analyse the correlation between the same expression or two different ones for the two people in the interactions: ", [1, 2], key=key)
        key += 1
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        expression_choicesA=list(real_tier_lists.keys())
        expression_choicesB=list(real_tier_lists.keys())
        if case_==1: 
            A_choice=st.radio("Expression to analyse:", expression_choicesA, key=key)
            key += 1
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            if real_tier_lists[A_choice]:
                width=st.slider("Select the width (period/window in ms to select): ", 1, 344, key='W1') 
                shift=st.slider("Select the shift (shift in ms of the selected window): ", 1, 344, key='S1') 
                fig=plot_correlation(get_correlation_folder(A_choice, databases_list, width, shift), databases_list)
                if fig!=None:
                    st.plotly_chart(fig)
                else:
                    st.write("No data to display")
            else:
                st.write("No data to display")
        else:
            A_choice=st.radio("Expression of person A to analyse:", expression_choicesA, key=key)
            key += 1
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            B_choice=st.radio("Expression of person B to analyse:", expression_choicesB, key=key)
            key += 1
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            if real_tier_lists[A_choice] and real_tier_lists[B_choice]:     
                width=st.slider("Select the width (period/window in ms to select): ", 1, 344, key='W2') 
                shift=st.slider("Select the shift (shift in ms of the selected window): ", 1, 344, key='S2') 
                fig=plot_correlation(get_correlation_folder(A_choice, databases_list, width, shift, B_choice), databases_list)
                if fig!=None:
                    st.plotly_chart(fig)
                else:
                    st.write("No data to display")
            else:
                st.write("No data to display")
        st.markdown(''' ''')
        st.markdown('''-----------------------------------------------------------------------------------------------------------------''')
        st.markdown(''' ''')
        st.subheader("********    By dataset and expression    ********")
        name_databases1=[key.replace('_paths','').upper() for key in databases.keys()]
        databases_1=[key for key in databases_pairs.keys()]
        databases_choice1=st.selectbox("Dataset choice: ", name_databases1, key=key)
        key += 1
        for i in range(len(databases_1)):
            if databases_choice1==databases_1[i].replace('_pairs','').upper():
                databases_list1=databases_pair_paths[databases_1[i]]

        st.markdown("Analysis of the correlation between two expressions or/and two entities during an interaction")
        st.markdown("Explanation:")
        st.markdown(" ")
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        expression_choicesA=list(real_tier_lists.keys())
        expression_choicesB=list(real_tier_lists.keys()) 
        A_choice=st.radio("Expression of person A to analyse:", expression_choicesA, key= key)
        key += 1
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        B_choice=st.radio("Expression of person B to analyse:", expression_choicesB, key= key)
        key += 1
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        case_choice=st.radio("Choose whether you want to analyse the correlation for one or two specific entities for the two people in the interactions: ", [1, 2], key=key)
        key += 1
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        if case_choice==1:
            case_choice1=st.radio("Do you want to study the correlation entity of A or B vs all entities of the other expression: ", ["A", "B"], key=key)
            key += 1
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            if case_choice1=="A":
                if real_tier_lists[A_choice]:
                    if real_tier_lists[A_choice]['Replace_Value'] != "" :
                        entity_levelA=[real_tier_lists[A_choice]['Replace_Value'], str("No_" + real_tier_lists[A_choice]['Replace_Value'])]
                    else :
                        entity_levelA=real_tier_lists[A_choice]['Intensities']
                    if real_tier_lists[A_choice]['Intensities']:
                        width=st.slider("Select the width (period/window in ms to select): ", 1, 344, key='W4') 
                        shift=st.slider("Select the shift (shift in ms of the selected window): ", 1, 344, key='S4')
                        entity1=st.radio("Entity of person A: ", entity_levelA, key='CE5')
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                        fig=plot_correlation(get_correlation_by_entity(A_choice, entity1, databases_list1, width, shift, B_choice), databases_list1)
                        if fig!=None:
                            st.plotly_chart(fig)
                        else:
                            st.write("No data to display")
                    else:
                        st.write("No data to display")
                else:
                    st.write("No data to display")
            else:
                if real_tier_lists[B_choice]:
                    if real_tier_lists[B_choice]['Replace_Value'] != "" :
                        entity_levelB=[real_tier_lists[B_choice]['Replace_Value'], str("No_" + real_tier_lists[B_choice]['Replace_Value'])]
                    else :
                        entity_levelB=real_tier_lists[B_choice]['Intensities']
                    if real_tier_lists[B_choice]['Intensities']:
                        width=st.slider("Select the width (period/window in ms to select): ", 1, 344, key='W5') 
                        shift=st.slider("Select the shift (shift in ms of the selected window): ", 1, 344, key='S5')
                        entity1=st.radio("Entity of person B: ", entity_levelB, key='CE6')
                        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                        fig=plot_correlation(get_correlation_by_entity(B_choice, entity1, databases_list1, width, shift, A_choice), databases_list1)
                        if fig!=None:
                            st.plotly_chart(fig)
                        else:
                            st.write("No data to display")
                    else:
                        st.write("No data to display")
        else :
            if real_tier_lists[A_choice] and real_tier_lists[B_choice]:
                if real_tier_lists[A_choice]['Replace_Value'] != "" :
                    entity_levelA=[real_tier_lists[A_choice]['Replace_Value'], str("No_" + real_tier_lists[A_choice]['Replace_Value'])]
                else :
                    entity_levelA=real_tier_lists[A_choice]['Intensities']
                if real_tier_lists[B_choice]['Replace_Value'] != "" :
                    entity_levelB=[real_tier_lists[B_choice]['Replace_Value'], str("No_" + real_tier_lists[B_choice]['Replace_Value'])]
                else :
                    entity_levelB=real_tier_lists[B_choice]['Intensities']
                if real_tier_lists[A_choice]['Intensities'] and real_tier_lists[B_choice]['Intensities']:
                    width=st.slider("Select the width (period/window in ms to select): ", 1, 344, key='W4') 
                    shift=st.slider("Select the shift (shift in ms of the selected window): ", 1, 344, key='S4')
                    entity1=st.radio("Entity of person A: ", entity_levelA, key='CE5')
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                    entity2=st.radio("Entity of person B: ", entity_levelB, key='CE6')
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                    fig=plot_correlation(get_correlation_byI(A_choice, entity1, databases_list1, width, shift, B_choice, entity2), databases_list1)
                    if fig!=None:
                        st.plotly_chart(fig)
                    else:
                        st.write("No data to display")
                else:
                    st.write("No data to display")
            else:
                st.write("No data to display")
        

    page3_names_to_funcs={
        "Individual Expression Sequences": page3_1,
        "Mimicry": page3_2,
        "Correlation": page3_3,
    }

    selected_page=st.sidebar.selectbox("Select a page", page3_names_to_funcs.keys())
    page3_names_to_funcs[selected_page]()

subprocess.run(["python", "..\\src\\snl_stats_extraction_data.py"])

if os.path.isfile('base_data.json') and os.path.getsize('base_data.json') > 0:
    st.error("You didn't choose tiers to anlayze. Go on Modify Tiers")
else :
    page3()