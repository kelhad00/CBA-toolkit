import subprocess
import streamlit as st
import os, sys, json
import Affichage_pattern
import time
script_path = os.path.realpath(os.path.dirname("src"))
os.chdir(script_path)
sys.path.append("..")

Affichage_pattern.affichage()

from src.page3.snl_stats_visualization_page3 import *
DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()

def page2():
    st.sidebar.markdown("Non Verbal Expressions Analysis")
    st.title("Non Verbal Expressions Analysis")
    st.markdown('''We look at the absolute duration and relative duration of each individual or interaction.
    \nAbsolute duration -> It means the sum of all difference of time 
    \nRelative duration -> It represents the percentage of the absolute duration''')
    #Scatters plots___________________________________________________
    def page2_1():
        #st.sidebar.markdown("Intra S&L analysis")
        st.title('Intra Expressions Analysis')
        st.markdown("It's an analysis based on each individual.")
        st.subheader('By dataset')

        expression_choices = list(tier_lists.keys())
        expression_choice = st.radio("Expression choice:", expression_choices)
        lst_ad = [f"scatter_plot_{expression_choice}", f"line_plot_{expression_choice}"]
        lst_rd=lst_ad
        name_databases = [key.split('_')[0].upper() for key in databases.keys()]
        figs_ad = st.selectbox("Absolute Duration Figures: ", lst_ad) 
        options = st.multiselect('Datasets list: ', name_databases, key = 1)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)   
        if tier_lists[expression_choice]: 
            list1= plot_intra_absolute_duration(options, expression_choice)
            for i in range(len(list1)) :
                for d in range(len(list1[i])) :
                    if figs_ad == lst_ad[d] :
                        if list1[i][d] != None :
                            st.write(list1[i][d])
                        else :
                            st.write("No Data available")
        else :
            st.write("No data available")
        

        figs_rd = st.selectbox("Relative Duration Figures: ", lst_ad) 
        options2 = st.multiselect('Datasets list: ', name_databases, key = 2)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        if tier_lists[expression_choice]:
            list2= plot_intra_relative_duration(options2, expression_choice)
            for k in range(len(list2)) :
                for l in range(len(list2[k])) :
                    if figs_rd == lst_rd[l] :
                        if list2[k][l] != None :
                            st.write(list2[k][l])
                        else :
                            st.write("No Data available")
        else :
            st.write("No data available")

        st.subheader('Basic statistics plots:')
        expression_choices_copy = expression_choices.copy()
        expression_choice_copy=st.radio("By expression:", expression_choices_copy)
        expression_values = list(tier_lists[expression_choice_copy])
        if expression_values : 
            expression_choice_2 = expression_choices_copy.copy()
            expression_choice_2.remove(expression_choice_copy)
            expression_choice_2 = st.radio("With:", expression_choice_2)
            if tier_lists[expression_choice_2]:
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                databases_lists = [values for values in databases_pair_paths.values()]
                database_choice=st.radio("Dataset choice: ", name_databases)
                lst_by_tier = [f"ad_plot_{expression_choice_copy.lower()}", f"rd_plot_{expression_choice_copy.lower()}"]
                for i in range(len(name_databases)):
                    if database_choice==name_databases[i]:
                        database_list_choice=databases_lists[i]
                figs_=st.selectbox(f"Figures {database_choice}: ", lst_by_tier) 
                for entity in expression_values :
                    try : 
                        lst_= plot_absolute_duration_from_tier_folder(database_list_choice, database_choice, expression_choice_copy, expression_choice_2, entity) + plot_relative_duration_from_tier_folder(database_list_choice, database_choice, expression_choice_copy, expression_choice_2, entity)
                        for i in range(len(lst_by_tier)):
                            if figs_ == lst_by_tier[i]:
                                if lst_[i] != None :
                                    st.write(lst_[i])
                                else :
                                    st.write("No Data available")
                    except :
                        st.write(f"No data available for: {entity} {expression_choice_copy}")
            else :
                st.write("No data available")
        else :
            st.write("No data available")

    def page2_2():
        #st.sidebar.markdown("Inter S&L analysis")
        st.header('Inter Expressions analysis')
        st.markdown("It's an analysis based on each interaction.")
        st.subheader('By dataset')
        lst_ab=['ad_scatter_plot_smiles', 'ad_line_plot_smiles', 'ad_scatter_plot_laughs', 'ad_line_plot_laughs']
        lst_rd=['rd_scatter_plot_smiles', 'rd_line_plot_smiles', 'rd_scatter_plot_laughs', 'rd_line_plot_laughs']
        lst_by_role=["ad smiles spk_vs_lsn",'ad laughs spk_vs_lsn','rd smiles spk_vs_lsn','rd laughs spk_vs_lsn',
        "ad smiles lsn_vs_spk",'ad laughs lsn_vs_spk','rd smiles lsn_vs_spk','rd laughs lsn_vs_spk']
        # lst_ab = ["ad_scatter_plot_tier", "ad_line_plot_tier"]
        # lst_rd = ["rd_scatter_plot_tier", "rd_line_plot_tier"]
        # lst_by_tier = ["ad_tier spk_vs_lsn", "rd_tier spk_vs_lsn", "ad_tier lsn_vs_spk", "rd_tier lsn_vs_spk"]
        name_databases=[key.split('_')[0].upper() for key in databases_paths.keys()]
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        figs_ab=st.selectbox("Absolute duration figures : ", lst_ab)
        options3 = st.multiselect('Datasets list : ', name_databases, key = 1)
        lst_1=plot_inter_absolute_duration(options3)
        for i in range(len(lst_1)):
            for d in range(len(lst_1[i])):
                if figs_ab == lst_ab[d]:
                    st.write(lst_1[i][d])
        figs_rd = st.selectbox("Relative duration Figures: ", lst_rd) 
        options4 = st.multiselect('Datasets list : ', name_databases, key = 2)

        lst_2=plot_inter_relative_duration(options4)
        for k in range(len(lst_2)):
            for l in range(len(lst_2[k])):
                if figs_rd == lst_rd[l]:
                    st.write(lst_2[k][l])

        st.subheader('By dataset and expression')
        expression_choices = list(tier_lists.keys())
        expression_choice=st.radio("By expression choice :", expression_choices)
        database_choice=st.radio("Database choice : ", name_databases)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        lst_roles=plot_inter_ad_spk_vs_lsn(database_choice)+plot_inter_rd_spk_vs_lsn(database_choice)+plot_inter_ad_lsn_vs_spk(database_choice)+plot_inter_rd_lsn_vs_spk(database_choice)
        # lst_tiers = plot_inter_ad_tier_spk_vs_lsn(database_choice, expression_choice) + plot_inter_rd_tier_spk_vs_lsn(database_choice, expression_choice) + plot_inter_ad_tier_lsn_vs_spk(database_choice, expression_choice) + plot_inter_rd_tier_lsn_vs_spk(database_choice, expression_choice)
        figs_roles=st.selectbox("Versus roles :", lst_by_role)
        for i in range(len(lst_by_role)):
            if figs_roles == lst_by_role[i]:
                st.write(lst_roles[i])

    page2_names_to_funcs = {
    "Intra S&L analysis": page2_1,
    "Inter S&L analysis": page2_2,}

    selected_page = st.sidebar.selectbox("Select a page", page2_names_to_funcs.keys())
    page2_names_to_funcs[selected_page]()

subprocess.run(["python", "..\\src\\snl_stats_extraction_data.py"])
page2()