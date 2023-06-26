import subprocess
import streamlit as st
import os, sys
import Affichage_pattern

Affichage_pattern.affichage()
script_path=os.path.realpath(os.path.dirname("src"))
os.chdir(script_path)
sys.path.append("..")


from src.page3.snl_stats_visualization_page3 import *
DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers=get_parameters()
real_tier_lists , real_tiers = get_parameters_tag()

def page2():
    st.sidebar.markdown("Non Verbal Expressions Analysis")
    st.title("Non Verbal Expressions Analysis")
    st.markdown('''We look at the absolute duration and relative duration of each individual (intra) or interaction (inter).''')
    st.markdown(''' ''')
    st.markdown('''Explanation of the statistics:''')
    st.write("<style>body { font-size: 14px; }</style><i>Absolute duration -> It means the sum of all difference of time over the entire video.</i>", unsafe_allow_html=True)
    st.write("<style>body { font-size: 14px; }</style><i>Relative duration -> It represents the percentage of the absolute duration compared to the total duration of the video.</i>", unsafe_allow_html=True)
    st.markdown(''' ''')
    st.markdown(''' ''')

    #Scatters plots___________________________________________________
    def page2_1():
        st.header('Intra Non Verbal Expressions Analysis')
        st.markdown("It's an analysis based on each individual. We look here at the sequence of expressions of each individual in each eaf file of the datasets.")

        st.subheader('Statistics by dataset')
        expression_choices=list(real_tier_lists.keys())
        expression_choice=st.radio("Expression choice:", expression_choices)
        lst_ad=[f"Scatter Plot {expression_choice}", f"Line Plot {expression_choice}"]
        lst_rd=lst_ad
        name_databases=[key.replace('_paths','').upper() for key in databases.keys()]
        figs_ad=st.selectbox("Absolute Duration Figures: ", lst_ad) 
        options=st.multiselect('Datasets list (you can select one or more): ', name_databases, key=1)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)   
        if real_tier_lists[expression_choice]: 
            list1=plot_intra_absolute_duration(options, expression_choice)
            for i in range(len(list1)):
                for d in range(len(list1[i])):
                    if isinstance(list1[i][d], pd.DataFrame):
                        if not list1[i][d].empty:
                            # Export csv 
                            csv_exp = list1[i][d].to_csv(index=False)
                            st.download_button(label="Download CSV file", data=csv_exp, file_name=f"{expression_choice.lower()}_intra_absolute_duration.csv", mime="text/csv")
                    else:    
                        if figs_ad==lst_ad[d]:
                            if list1[i][d]!=None:
                                st.write(list1[i][d])
                            else:
                                st.write("No Data available")
        else:
            st.write("No data available")
        figs_rd=st.selectbox("Relative Duration Figures: ", lst_ad) 
        options2=st.multiselect('Datasets list (you can select one or more): ', name_databases, key=2)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        if real_tier_lists[expression_choice]:
            list2=plot_intra_relative_duration(options2, expression_choice)
            for k in range(len(list2)):
                for l in range(len(list2[k])):
                    if isinstance(list2[k][l], pd.DataFrame):
                        if not list2[k][l].empty:
                            # Export csv 
                            csv_exp = list2[k][l].to_csv(index=False)
                            st.download_button(label="Download CSV file", data=csv_exp, file_name=f"{expression_choice.lower()}_intra_relative_duration.csv", mime="text/csv")
                    else:
                        if figs_rd==lst_rd[l]:
                            if list2[k][l]!=None:
                                st.write(list2[k][l])
                            else:
                                st.write("No Data available")
        else:
            st.write("No data available")
        st.markdown(''' ''')
        st.markdown('''-----------------------------------------------------------------------------------------------------------------''')
        st.markdown(''' ''')
        st.subheader('Statistics divided by expressions')
        expression_choices_copy=expression_choices.copy()
        expression_choice_copy=st.radio("Divided by expression: ", expression_choices_copy)
        if real_tier_lists[expression_choice_copy]['Replace_Value'] != "" :
            expression_values = [real_tier_lists[expression_choice_copy]['Replace_Value'], str("No_"+real_tier_lists[expression_choice_copy]['Replace_Value'])]
        else :
            expression_values=real_tier_lists[expression_choice_copy]['Intensities']
        if expression_values: 
            expression_choice_2=expression_choices_copy.copy()
            expression_choice_2.remove(expression_choice_copy)
            expression_choice_2=st.radio("Expression to analyse: ", expression_choice_2)
            if real_tier_lists[expression_choice_2]:
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                databases_lists=[values for values in databases_pair_paths.values()]
                database_choice=st.radio("Dataset choice: ", name_databases)
                lst_by_tier=[f"Absolute Duration {expression_choice_2.lower()}", f"Relative Duration {expression_choice_2.lower()}"]
                for i in range(len(name_databases)):
                    if database_choice==name_databases[i]:
                        database_list_choice=databases_lists[i]
                figs_=st.selectbox(f"Figures {database_choice}: ", lst_by_tier) 
                for entity in expression_values:
                    try : 
                        lst_=plot_absolute_duration_from_tier_folder(database_list_choice, database_choice, expression_choice_copy, expression_choice_2, entity) + plot_relative_duration_from_tier_folder(database_list_choice, database_choice, expression_choice_copy, expression_choice_2, entity)
                        if figs_==f"Absolute Duration {expression_choice_2.lower()}":
                            file_name = f"{expression_choice_2.lower()}_vs_{entity.lower()}_{expression_choice_copy.lower()}_intra_absolute_duration.csv"
                            if lst_[0] is not None:
                                st.write(lst_[0])
                            else:
                                st.write("No Data available")
                            if isinstance(lst_[1], pd.DataFrame):
                                if not lst_[1].empty:
                                    # Export csv 
                                    csv_exp = lst_[1].to_csv(index=False)
                                    st.download_button(label="Download CSV file", data=csv_exp, file_name=file_name, mime="text/csv")
                        elif figs_==f"Relative Duration {expression_choice_2.lower()}":
                            file_name = f"{expression_choice_2.lower()}_vs_{entity.lower()}_{expression_choice_copy.lower()}_intra_relative_duration.csv"
                            if lst_[2] is not None:
                                st.write(lst_[i])
                            else:
                                st.write("No Data available")
                            if isinstance(lst_[3], pd.DataFrame):
                                if not lst_[3].empty:
                                    # Export csv 
                                    csv_exp = lst_[3].to_csv(index=False)
                                    st.download_button(label="Download CSV file", data=csv_exp, file_name=file_name, mime="text/csv")
                    except:
                        st.write(f"No data available for: {entity} {expression_choice_copy}")
            else:
                st.write("No data available")
        else:
            st.write("No data available")

    def page2_2():
        #st.sidebar.markdown("Inter S&L analysis")
        st.header('Inter Non Verbal Expressions Analysis')
        st.markdown("It's an analysis based on each interaction between two persons. All figures are based on the duration of the expressions of each interaction (so two files) in the datasets.")

        st.subheader('Statistics by dataset')
        expression_choices1=list(real_tier_lists.keys())
        expression_choice1=st.radio("Expression choice:", expression_choices1)
        lst_ab=[f"Scatter Plot {expression_choice1}", f"Line Plot {expression_choice1}"]
        lst_rd=[f"Scatter Plot {expression_choice1}", f"Line Plot {expression_choice1}"]
        name_databases=[key.replace('_paths','').upper() for key in databases_paths.keys()]
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        figs_ab=st.selectbox("Absolute Duration Figures : ", lst_ab)
        options3=st.multiselect('Datasets list (you can select one or more): ', name_databases, key=1)
        if real_tier_lists[expression_choice1]:
            lst_1=plot_inter_absolute_duration(options3, expression_choice1)
            for i in range(len(lst_1)):
                for d in range(len(lst_1[i])):
                    if isinstance(lst_1[i][d], pd.DataFrame):
                        if not lst_1[i][d].empty:
                            # Export csv 
                            csv_exp = lst_1[i][d].to_csv(index=False)
                            st.download_button(label="Download CSV file", data=csv_exp, file_name=f"{expression_choice1.lower()}_inter_absolute_duration.csv", mime="text/csv")
                    else:
                        if figs_ab==lst_ab[d]:
                            if lst_1[i][d]!=None : 
                                st.write(lst_1[i][d])
                            else:
                                st.write("No Data available")
        else:
            st.write("No data available")
        figs_rd=st.selectbox("Relative Duration Figures: ", lst_rd) 
        options4=st.multiselect('Datasets list (you can select one or more): ', name_databases, key = 2)
        if tier_lists[expression_choice1]:
            lst_2=plot_inter_relative_duration(options4, expression_choice1)
            for k in range(len(lst_2)):
                for l in range(len(lst_2[k])):
                    if isinstance(lst_2[k][l], pd.DataFrame):
                        if not lst_2[k][l].empty:
                            # Export csv 
                            csv_exp = lst_2[k][l].to_csv(index=False)
                            st.download_button(label="Download CSV file", data=csv_exp, file_name=f"{expression_choice1.lower()}_inter_relative_duration.csv", mime="text/csv")
                    else:
                        if figs_rd == lst_rd[l]:
                            if lst_2[k][l]!=None:
                                st.write(lst_2[k][l])
                            else:
                                st.write("No Data available")
        else:
            st.write("No data available")
        st.markdown(''' ''')
        st.markdown('''-----------------------------------------------------------------------------------------------------------------''')
        st.markdown(''' ''')
        st.subheader('Statistics divided by expressions for a specific dataset')
        st.markdown("We are looking at the stats of a specific expression to analyse compare to another one during an interaction. Each graph will be divided to compare the entities of first expression vs 2 entity of the other expression. The first expression will be the one you choose in the second radio button. The second expression will be the one you choose in the first radio button. ")
        expression_choices_copy1=expression_choices1.copy()
        expression_choice_copy1=st.radio("Divided by expression: ", expression_choices_copy1)
        if real_tier_lists[expression_choice_copy1]['Replace_Value'] != "" :
            expression_values1 = [real_tier_lists[expression_choice_copy1]['Replace_Value'], str("No_"+real_tier_lists[expression_choice_copy1]['Replace_Value'])]
        else :
            expression_values1=real_tier_lists[expression_choice_copy1]['Intensities']
        if expression_values1:
            expression_choice2=expression_choices_copy1.copy()
            expression_choice2.remove(expression_choice_copy1)
            expression_choice2=st.radio("Expression to analyse: ", expression_choice2)
            database_choice=st.radio("Dataset choice: ", name_databases)
            lst_by_tier=[]
            lst_by_tier.append(f"Absolute duration {expression_choice2.lower()}")
            lst_by_tier.append(f"Relative duration {expression_choice2.lower()}")
            figs_roles=st.selectbox("Figures:", lst_by_tier)
            for entity1 in expression_values1:
                expression_values2=expression_values1.copy()
                # expression_values2.remove(entity1)
                if expression_values2:
                    for entity2 in expression_values2:
                        try: 
                            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                            lst_tiers=plot_inter_ad_entity1_vs_entity2_tier(database_choice, expression_choice_copy1, expression_choice2, entity1, entity2)+plot_inter_rd_entity1_vs_entity2_tier(database_choice, expression_choice_copy1, expression_choice2, entity1, entity2)
                            if figs_roles == f"Absolute duration {expression_choice2.lower()}":
                                file_name = f"{expression_choice2.lower()}_during_{entity1.lower()}_vs_{entity2.lower()}_{expression_choice_copy1.lower()}_inter_absolute_duration.csv"
                                if lst_tiers[0] is not None:
                                    st.write(lst_tiers[0])
                                else:
                                    st.write("No Data available")
                                if isinstance(lst_tiers[1], pd.DataFrame):
                                    if not lst_tiers[1].empty:
                                        # Export csv 
                                        csv_exp = lst_tiers[1].to_csv(index=False)
                                        st.download_button(label="Download CSV file", data=csv_exp, file_name=file_name, mime="text/csv")
                            elif figs_roles == f"Relative duration {expression_choice2.lower()}":
                                file_name = f"{expression_choice2.lower()}_during_{entity1.lower()}_vs_{entity2.lower()}_{expression_choice_copy1.lower()}_inter_relative_duration.csv"
                                if lst_tiers[2] is not None:
                                    st.write(lst_tiers[2])
                                else:
                                    st.write("No Data available")
                                if isinstance(lst_tiers[3], pd.DataFrame):
                                    if not lst_tiers[3].empty:
                                        # Export csv 
                                        csv_exp = lst_tiers[3].to_csv(index=False)
                                        st.download_button(label="Download CSV file", data=csv_exp, file_name=file_name, mime="text/csv")
                        except:
                            st.write(f"No data available for: {expression_choice2.lower()} during {entity1} {expression_choice_copy1} versus {entity2} {expression_choice_copy1}")
        else:
            st.write("No data available")

    page2_names_to_funcs={
    "Intra Non Verbal Expressions Analysis": page2_1,
    "Inter Non Verbal Expressions Analysis": page2_2,}

    selected_page=st.sidebar.selectbox("Select a page", page2_names_to_funcs.keys())
    page2_names_to_funcs[selected_page]()

subprocess.run(["python", "..\\src\\snl_stats_extraction_data.py"])

if os.path.isfile('base_data.json') and os.path.getsize('base_data.json') > 26:
    subprocess.run(["python", "..\\src\\snl_stats_extraction_data.py"])
    page2()
else :
    st.error("You didn't choose tiers to anlayze. Go on Modify Tiers")