import subprocess
import streamlit as st
import os, sys
import Affichage_pattern

Affichage_pattern.affichage()
script_path=os.path.realpath(os.path.dirname("src"))
os.chdir(script_path)
sys.path.append("..")

from src.page2.snl_stats_visualization_page2 import *
from src.page2.snl_stats_visualization_page6 import *
from src.page2.snl_stats_visualization_database import *
DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers=get_parameters()
real_tier_lists , real_tiers = get_parameters_tag()

def page1():
    st.sidebar.markdown("Descriptive analysis")
    st.title('Descriptive analysis of the database')

    def page1_1() :
        st.sidebar.markdown("Database Information")
        st.header('Database Information')
        name_databases=[key.replace('_paths','').upper() for key in databases.keys()]
        databases_=[value for value in databases_pair_paths.values()]
        databases_choice=st.selectbox("Dataset choice: ", name_databases)
        name_tiers=list(real_tier_lists.keys())+["GENERAL"]
        tiers_choice=st.selectbox("Expression choice:", name_tiers, index=name_tiers.index("GENERAL"))
        for i in range(len(name_databases)):
            if databases_choice==name_databases[i]:
                databases_choice=databases_[i]
        if tiers_choice=='GENERAL':
            data=display_general_informations_files(databases_choice)
            columns_names=["Filename", "Duration"]+list(real_tier_lists.keys())
            df=pd.DataFrame(data, columns=columns_names)
            st.table(df)
        else:
            if real_tier_lists[tiers_choice]['Replace_Value'] != "":
                data=display_specific_informations(databases_choice, tiers_choice, [real_tier_lists[tiers_choice]['Replace_Value'], str("No_" + real_tier_lists[tiers_choice]['Replace_Value'])], 'Replace_Value')
                columns_names=["Filename", "Min duration", "Max duration"]+[real_tier_lists[tiers_choice]['Replace_Value'], str("No_" + real_tier_lists[tiers_choice]['Replace_Value'])]
                df=pd.DataFrame(data, columns=columns_names)
                st.write(df)
            else:
                data=display_specific_informations(databases_choice, tiers_choice, real_tier_lists[tiers_choice]['Intensities'], 'Intensities')
                columns_names=["Filename", "Min duration", "Max duration"]+real_tier_lists[tiers_choice]['Intensities']
                df=pd.DataFrame(data, columns=columns_names)
                st.write(df)
    def page1_2():
        st.sidebar.markdown("Expression Per Minute")
        # # #Barplots ______________________________________________________
        st.header('Expression Per Minute')
        st.markdown("We count the number of expressions/tiers we have in one minute in each dataset.")
        st.markdown(''' ''')
        name_databases=[key.replace('_paths','').upper() for key in databases.keys()]
        databases_=[value for value in databases_pair_paths.values()]
        databases_choice=st.selectbox("Dataset choice: ", name_databases)
        for i in range(len(name_databases)):
            if databases_choice==name_databases[i]:
                databases_choice=databases_[i]
        if st.checkbox("All entities"):
            expression_choice=st.radio("Expression to see: ", list(real_tier_lists.keys()), key="E1")
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            expression_choice=expression_choice
            choices_case=["Intra (per file/individual)","Inter (per interaction)"]
            case_choice=st.radio("Choice: ", choices_case)
            case_list=[None, 2]
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            for _ in range(len(case_list)):
                if case_choice==choices_case[_]:
                    case_choice=case_list[_]
            if (plot_expression_per_min(databases_choice, expression_choice, case_choice)==None):
                st.write("No data available")
            else:
                st.plotly_chart(plot_expression_per_min(databases_choice, expression_choice, case_choice))
        if st.checkbox("By entity"):
            expression_choice=st.radio("Expression to see: ", list(real_tier_lists.keys()), key="E2")
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            if real_tier_lists[expression_choice]['Replace_Value'] != "" :
                 entity_choice=st.radio("Entity of the chosen expression: ", [real_tier_lists[expression_choice]['Replace_Value'], str("No_" + real_tier_lists[expression_choice]['Replace_Value'])])
            else :
                entity_choice = st.radio("Entity of the chosen expression: ", real_tier_lists[expression_choice]['Intensities'])
            if entity_choice is not None:
                if (plot_expression_per_min_I(databases_choice, expression_choice, entity_choice)==None) :
                    st.write("No data available")
                else:
                    st.write(plot_expression_per_min_I(databases_choice, expression_choice, entity_choice))
            else:
                st.write("No data available")
    def page1_3():
        st.header('Basic statistics on non verbal expressions')
        st.markdown('''We look at the maximum, minimum, mean, median and standard deviation on the database.''')
        st.markdown(''' ''')
        st.markdown('''Explanation of the statistics:''')
        st.write("<style>body { font-size: 14px; }</style><i>Absolute duration -> It means the sum of all difference of time over the entire video.</i>", unsafe_allow_html=True)
        st.write("<style>body { font-size: 14px; }</style><i>Relative duration -> It represents the percentage of the absolute duration compared to the total duration of the video.</i>", unsafe_allow_html=True)
        st.markdown(''' ''')
        st.markdown(''' ''')
        st.subheader('Statistics by dataset')
        name_list=["Absolute duration", "Relative duration"]
        expression_choices=list(real_tier_lists.keys())
        expression_choices.append('all')
        expression_choice=st.radio("Expression choice:", expression_choices)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        name_databases=[key.replace('_paths','').upper() for key in databases.keys()]
        figs=st.selectbox("Figures: ", name_list) 
        choice_list=["Standard deviation", "Mean", "Median", "Max", "Min", "All"]
        choice=st.radio("Which feature do you want see?  ", choice_list)
        if expression_choice!='all':
            if real_tier_lists[expression_choice]:
                if figs=='Absolute duration':
                    fig1_0=plot_absolute_duration(expression_choice, choice, name_databases)
                    if fig1_0!=None:    
                        st.write(fig1_0)
                    else:
                        st.write(f"No Data available for {expression_choice}")
                else:
                    fig2_0=plot_relative_duration(expression_choice, choice, name_databases)
                    if fig2_0!=None:
                        st.write(fig2_0)
                    else:
                        st.write(f"No Data available for {expression_choice}")
            else:
                st.write(f"No Data available for {expression_choice}")
        elif expression_choice=='all': 
            figures1=[]
            if figs=='Absolute duration':
                fig1_1=plot_absolute_duration(expression_choice, choice, name_databases)
                figures1.extend(fig1_1)
            else: 
                fig2_1=plot_relative_duration(expression_choice, choice, name_databases)
                figures1.extend(fig2_1)
            for fig in figures1:
                if fig!=None:
                    st.write(fig)
                else:
                    st.write("No Data available")
        st.markdown(''' ''')
        st.markdown('''-----------------------------------------------------------------------------------------------------------------''')
        st.markdown(''' ''')
        st.subheader('Statistics divided by expressions:')  
        expression_choices_1=expression_choices.copy()
        expression_choices_1.remove('all')
        expression_choice_1=st.radio("Divided by expression: ", expression_choices_1)
        if real_tier_lists[expression_choice_1]['Replace_Value'] != "" :
            expression_values = [real_tier_lists[expression_choice_1]['Replace_Value'], str("No_"+real_tier_lists[expression_choice_1]['Replace_Value'])]
        else :
            expression_values=real_tier_lists[expression_choice_1]['Intensities']
        if expression_values:
            name_list_by_expression_kind1=[f"Absolute duration from {expression_choice_1.lower()}"]
            name_list_by_expression_kind2=[f"Relative duration from {expression_choice_1.lower()}"]
            name_list_by_expression=name_list_by_expression_kind1+name_list_by_expression_kind2
            expression_choices_copy=expression_choices.copy()
            expression_choices_copy.remove(expression_choice_1) 
            expression_choice_copy=st.radio("Expression to analyse: ", expression_choices_copy)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            count=0
            figs1=st.selectbox("Figures: ", name_list_by_expression) 
            choice_list1=["Standard deviation", "Mean", "Median", "Max", "Min", "All"]
            choice1=st.radio("Which feature do you want see?  ", choice_list1, key = count)
            if expression_choice_copy!='all':
                if real_tier_lists[expression_choice_copy]:
                    if "Absolute" in figs1:
                        count+=1
                        for entity in expression_values:
                            fig1_temp=plot_absolute_duration_from_tier(expression_choice_1, entity, expression_choice_copy, choice1, name_databases)
                            if fig1_temp!=None:
                                st.write(fig1_temp)    
                            else:
                                st.write(f"No data available for: {entity} {expression_choice_1}")
                    elif "Relative" in figs1:
                        count+=1
                        for entity in expression_values:
                            fig1_temp=plot_relative_duration_from_tier(expression_choice_1, entity, expression_choice_copy, choice1, name_databases)
                            if fig1_temp!=None:
                                st.write(fig1_temp)
                            else: 
                                st.write(f"No data available for: {entity} {expression_choice_1}")
                else:
                    st.write(f"No data available for {expression_choice_copy} with {expression_choice_1}")
            elif expression_choice_copy=='all': 
                figures=[]
                if "Absolute" in figs1:
                    count+=1
                    for entity in expression_values:
                        fig1_temp=plot_absolute_duration_from_tier(expression_choice_1, entity, expression_choice_copy, choice1, name_databases)
                        figures.extend(fig1_temp)
                elif "Relative" in figs1:
                    count+=1
                    for entity in expression_values:
                        fig1_temp=plot_relative_duration_from_tier(expression_choice_1, entity, expression_choice_copy, choice1, name_databases)
                        figures.extend(fig1_temp)
                for fig_R in figures: 
                    if fig_R!=None:
                        st.write(fig_R)
                    else:
                        st.write("No Data available")
        else:
            st.write(f"No data available for {expression_choice_1}")
    
    page1_names_to_funcs={
    "Database Information": page1_1,
    "Expression Per Minute": page1_2,
    "Stats On Non Verbal Expressions": page1_3,}

    selected_page=st.sidebar.selectbox("Select a page", page1_names_to_funcs.keys())
    page1_names_to_funcs[selected_page]()

if os.path.isfile('base_data.json') and os.path.getsize('base_data.json') > 26:
    subprocess.run(["python", "..\\src\\snl_stats_extraction_data.py"])
    print("Sah : ", os.path.getsize('base_data.json'))
    page1()
else :
    st.error("You didn't choose tiers to anlayze. Go on Modify Tiers")