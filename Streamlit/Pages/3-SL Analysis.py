
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


def page2():
    st.sidebar.markdown("S&L Analysis")
    st.title("S&L Analysis")
    st.markdown('''We look at the absolute duration and relative duration of each individual or interaction.
    \nAbsolute duration -> It means the sum of all difference of time 
    \nRelative duration -> It represents the percentage of the absolute duration''')
    #Scatters plots___________________________________________________
    def page2_1():
        #st.sidebar.markdown("Intra S&L analysis")
        st.title('Intra S&L analysis')
        st.markdown("It's an analysis based on each individual.")
        st.subheader('By datasets')

        lst_ad=['scatter_plot_smiles', 'line_plot_smiles', 'scatter_plot_laughs', 'line_plot_laughs']
        lst_rd=lst_ad
        lst_by_role=["ad_plot_smiles_lsn", "ad_plot_laughs_lsn","ad_plot_smiles_spk", "ad_plot_laughs_spk","rd_plot_smiles_lsn", "rd_plot_laughs_lsn","rd_plot_smiles_spk", "rd_plot_laughs_spk"]
        name_databases=['ccdb', 'ifadv', 'ndc']

        figs_ad = st.selectbox("Absolute duration Figures: ", lst_ad) 
        database_choice=st.radio("Database choice ->", ['ccdb', 'ifadv', 'ndc'])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        list1= plot_intra_absolute_duration(database_choice)
        for i in range(len(lst_ad)):
            if figs_ad == lst_ad[i]:
                st.write(list1[i])

        # fig_choice=st.radio(label="Figures :", options=lst_ad)
        # st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        # for i in range(len(lst_ad)):
        #     if fig_choice==lst_ad[i]:
        #         st.plotly_chart(list1[i])

        figs_rd = st.selectbox("Relative duration Figures: ", lst_ad) 
        database_choice=st.radio("Database choice -> ", ['ccdb', 'ifadv', 'ndc'])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        list2= plot_intra_relative_duration(database_choice)
        for i in range(len(lst_rd)):
            if figs_rd == lst_rd[i]:
                st.write(list2[i])


        st.subheader('By role')
        #st.text("On CCDB")
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        databases_lists=[ccdb_paths, ifadv_paths, ndc_paths]
        database_choice=st.radio("Database choice --> ", name_databases)
        for i in range(3):
            if database_choice==name_databases[i]:
                database_list_choice=databases_lists[i]
        lst_=plot_absolute_duration_from_lsn_folder(database_list_choice,database_choice)+plot_absolute_duration_from_spk_folder(database_list_choice,database_choice)+plot_relative_duration_from_lsn_folder(database_list_choice,database_choice)+plot_relative_duration_from_spk_folder(database_list_choice,database_choice)
        figs_=st.selectbox(f"Figures {database_choice}: ", lst_by_role) 
        for i in range(len(lst_by_role)):
            if figs_ == lst_by_role[i]:
                st.write(lst_[i])

    def page2_2():
        #st.sidebar.markdown("Inter S&L analysis")
        st.header('Inter S&L analysis')
        st.markdown("It's an analysis based on each interaction.")
        st.subheader('By dataset')
        lst_=['ad_scatter_plot_smiles', 'ad_line_plot_smiles', 'ad_scatter_plot_laughs', 'ad_line_plot_laughs',
        'rd_scatter_plot_smiles', 'rd_line_plot_smiles', 'rd_scatter_plot_laughs', 'rd_line_plot_laughs']
        lst_by_role=["ad smiles spk_vs_lsn",'ad laughs spk_vs_lsn','rd smiles spk_vs_lsn','rd laughs spk_vs_lsn',
        "ad smiles lsn_vs_spk",'ad laughs lsn_vs_spk','rd smiles lsn_vs_spk','rd laughs lsn_vs_spk']
        name_databases=['ccdb', 'ifadv', 'ndc']

        database_choice=st.radio("Database choice --> ", name_databases)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        lst=plot_inter_absolute_duration(database_choice)+plot_inter_relative_duration(database_choice)
        figs=st.selectbox("Absolute and relative duration figures : ", lst_)
        for i in range(len(lst_)):
            if figs == lst_[i]:
                st.write(lst[i])

        st.subheader('By dataset and role')
        database_choice=st.radio("Database choice -->", name_databases)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        lst_roles=plot_inter_ad_spk_vs_lsn(database_choice)+plot_inter_rd_spk_vs_lsn(database_choice)+plot_inter_ad_lsn_vs_spk(database_choice)+plot_inter_rd_lsn_vs_spk(database_choice)
        figs_roles=st.selectbox("Versus roles :", lst_by_role)
        for i in range(len(lst_by_role)):
            if figs_roles == lst_by_role[i]:
                st.write(lst_roles[i])

    page2_names_to_funcs = {
    "Intra S&L analysis": page2_1,
    "Inter S&L analysis": page2_2,}

    selected_page = st.sidebar.selectbox("Select a page", page2_names_to_funcs.keys())
    page2_names_to_funcs[selected_page]()

page2()