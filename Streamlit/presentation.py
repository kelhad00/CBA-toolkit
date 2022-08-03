import streamlit as st
import os, sys, json
script_path = os.path.realpath(os.path.dirname("SNL_Stats"))
os.chdir(script_path)
sys.path.append("..")

from ML_stats.ml_stats import *
from ML_stats.ml_stats_vizualisation import *
from ML_stats.settings import *
from SNL_Stats.snl_stats_visualization import *


#______________________________________________________________________________________________
# Here it's just to make watching more fun. 
# You just have to put a music in the Streamlit folder (I mean the same directory as this python file).

# st.markdown('Listen to this _beautiful song_ while you are exploring this interactive page ! ')
# st.markdown("Song : _Tilte_ by **_Artist name_**")
# audio_file = open('music_name.mp3','rb')
# audio_bytes = audio_file.read()
# st.audio(audio_bytes, format='audio/mp3')

def main_page():
    #st.markdown("# Main page")
    st.sidebar.markdown("Main page")
    st.title('Smiles and Laughs Study ')
    st.markdown('''This is an interactive web page where we are going to show some statistics based on a given database.
    \nThis database contains for the moment three datasets : CCDB, IFADV and NDC. Each dataset has files containing smiles and laughs. 
    \nWe explored these smiles and laughs and we tried to know which kind of effects they could have on a person or during an interaction.
    \n\nNow look at each page of the web page !''')

def page1():
    st.sidebar.markdown("Descriptive analysis")
    # #Barplots ______________________________________________________
    st.title('Descriptive analysis')
    st.header('Basic statistics on smiles and laughs')
    st.markdown("We look at the mean, median and standard deviation on the database.")
    st.subheader('By datasets')

    name_list=["absolute duration", "relative duration"]
    name_list_by_role=["absolute duration spk","absolute duration lsn","relative duration spk","relative duration lsn" ]
    expression_choice=st.radio("Expression choice ->", ['smiles', 'laughs'])
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    fig1 = plot_absolute_duration(expression_choice)
    fig2 = plot_relative_duration(expression_choice)
    L=[fig1, fig2]
    figs=st.selectbox(" Basic statistics plots : ", name_list) 
    
    for i in range(len(name_list)):
        if figs == name_list[i]:
            st.write(L[i])

    st.subheader('By role')
    expression_choice=st.radio("Expression choice->", ['smiles', 'laughs'])
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    L=[plot_absolute_duration_from_spk(expression_choice), plot_absolute_duration_from_lsn(expression_choice), 
    plot_relative_duration_from_spk(expression_choice), plot_relative_duration_from_lsn(expression_choice)]
    figs=st.selectbox(" Basic statistics plots by role - Absolute duration : ", name_list_by_role) 
    for i in range(len(name_list_by_role)):
        if figs == name_list_by_role[i]:
            st.write(L[i])

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

def page3():
    st.sidebar.markdown("S&L Effects")
    st.title('Effects analysis')
    st.markdown('''In this part, we want to know if an expression has an effect on another one.''')

    def page3_1():
        st.title('Intra S&L effects')
        st.subheader('Smiles & Laughs Track')
        text_='''Here, we are checking what is before and after an expression in ploting percentage of the preceded and next expression.
        \n Track choice --> The expression we want to study
        \n Check choice --> Expression before and after the track choice.
        
        \nNB : These cases dont work for the moment. 
        \nTrack choice = S & Check choice = L     and    Track choice = S & Check choice = S'''
        st.markdown(text_)
        track_choice=st.radio("Track choice ->", ['L', 'S'])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        check_choice=st.radio("Check choice ->", ['L', 'S'])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        # #st.subheader('Previous')
        fig1= plot_track_previous_SL(SL_track(check_choice,track_choice, DIR))
        fig2= plot_track_following_SL(SL_track(check_choice,track_choice, DIR))
        st.plotly_chart(fig1)
        # #st.subheader('Following')
        st.plotly_chart(fig2) 

        st.subheader('Smiles & Laughs Track by intensity')
        st.markdown("We do the same action as before but taking into account the intensities.")
        track_choice=st.radio("Track choice :", ['L', 'S'])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        check_choice=st.radio("Check choice :", ['L', 'S'])
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        # #st.subheader('Previous')
        fig1= plot_track_previous_SL_byI(SL_track_byI(check_choice,track_choice,DIR)[0])
        fig2= plot_track_following_SL_byI(SL_track_byI(check_choice,track_choice,DIR)[1])
        st.plotly_chart(fig1)
        # #st.subheader('Following')
        st.plotly_chart(fig2) 

    def page3_2():
        st.header('Inter S&L effects')
        st.subheader("Mimicry")
        st.markdown("We look at the capacity of someone to mimic someone else. ( A / B -> B mimic A)")
        name_databases=['CCDB','IFADV','NDC']
        databases_=[ccdb_pair, ifadv_pair, ndc_pair]
        databases_choice=st.selectbox("Databases list :", name_databases)
        for i in range(len(name_databases)):
            if databases_choice==name_databases[i]:
                databases_choice=databases_[i]

        st.subheader('For Smiles / Smiles')
        if st.checkbox("All intensities for smiles"):
            fig=plot_mimicry(give_mimicry_folder1(get_smiles_dict_conv_folder, databases_choice))
            st.plotly_chart(fig)
            st.text("Do you want to filter by role ?")
            role_choice=st.radio(label="Choice :", options=["Yes", "No"])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

            if role_choice == "Yes":
                roles=st.multiselect("Roles :", ["spk","lsn"])
                for i in roles :
                    fig=plot_mimicry(give_mimicry_folder1(eval('get_smiles_from_'+i+'_folder'), databases_choice))
                    st.write("For ",i," :")
                    st.plotly_chart(fig)
            else:
                pass
        if st.checkbox("By intensity _ s"): 
            if st.checkbox("For one intensity :  "):
                intensities_smiles = st.multiselect("Intensities :", ["SUBTLE", "LOW", "MEDIUM", "HIGH"])
                for i in intensities_smiles:
                    st.write(i, "smiles mimic ", i, "smiles : " )
                    fig = plot_mimicry(give_mimicry_folder1(get_smiles_dict_conv_folder, databases_choice, 'Intensity', str.lower(i) ))
                    st.plotly_chart(fig)
                    st.text("Do you want to filter by role ?")
                    role_choice=st.radio(label="Choice :   ", options=["Yes", "No"])
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                    if role_choice == "Yes":
                        roles=st.multiselect("Roles :   ", ["spk","lsn"])
                        for j in roles :
                            fig=plot_mimicry(give_mimicry_folder1(eval('get_smiles_from_'+j+'_folder'), databases_choice, 'Intensity', str.lower(i)))
                            st.write("For ",j," :")
                            st.plotly_chart(fig)
                    else:
                        pass
            if st.checkbox("For two intensities :  "):
                intensities_smiles = st.multiselect("Intensities :", ["SUBTLE", "LOW", "MEDIUM", "HIGH"])
                st.write(intensities_smiles[1], "smiles mimic ", intensities_smiles[0], "smiles : " )
                fig = plot_mimicry(give_mimicry_folder1(get_smiles_dict_conv_folder, databases_choice, 'Intensity', 
                [str.lower(intensities_smiles[0]), str.lower(intensities_smiles[1])] ))
                st.plotly_chart(fig)
                st.text("Do you want to filter by role ?")
                role_choice=st.radio(label="Choice :     ", options=["Yes", "No"])
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                if role_choice == "Yes":
                    roles=st.multiselect("Roles :      ", ["spk","lsn"])
                    for j in roles :
                        fig=plot_mimicry(give_mimicry_folder1(eval('get_smiles_from_'+j+'_folder'), databases_choice, 'Intensity', [str.lower(intensities_smiles[0]), str.lower(intensities_smiles[1])]))
                        st.write("For ",j," :")
                        st.plotly_chart(fig)
                else:
                    pass

        st.subheader('For Laughs / Laughs ')
        if st.checkbox("All intensities for laughs"):
            fig=plot_mimicry(give_mimicry_folder1(get_laughs_dict_conv_folder, databases_choice))
            st.plotly_chart(fig)
            st.text("Do you want to filter by role ?")
            role_choice=st.radio(label="Choice  :", options=["Yes", "No"])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

            if role_choice == "Yes":
                roles=st.multiselect("Roles  :", ["spk","lsn"])
                for i in roles :
                    fig=plot_mimicry(give_mimicry_folder1(eval('get_laughs_from_'+i+'_folder'), databases_choice))
                    st.write("For ",i," :")
                    st.plotly_chart(fig)
            else:
                pass   
        if st.checkbox("By intensity _ l"): 
            if st.checkbox("For one intensity :"):
                intensities_laughs = st.multiselect("Intensities :", ["LOW", "MEDIUM", "HIGH"])
                for i in intensities_laughs:
                    st.write(i, "laughs mimic ", i, "laughs : " )
                    fig = plot_mimicry(give_mimicry_folder1(get_laughs_dict_conv_folder, databases_choice, 'Intensity', str.lower(i) ))
                    st.plotly_chart(fig)
                    st.text("Do you want to filter by role ?")
                    role_choice=st.radio(label="Choice:   ", options=["Yes", "No"])
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                    if role_choice == "Yes":
                        roles=st.multiselect("Roles:   ", ["spk","lsn"])
                        for j in roles :
                            fig=plot_mimicry(give_mimicry_folder1(eval('get_laughs_from_'+j+'_folder'), databases_choice, 'Intensity', str.lower(i)))
                            st.write("For ",j," :")
                            st.plotly_chart(fig)
                    else:
                        pass
            if st.checkbox("For two intensities :"):
                intensities_laughs = st.multiselect("Intensities :", ["LOW", "MEDIUM", "HIGH"])
                st.write(intensities_laughs[1], "laughs mimic ", intensities_laughs[0], "laughs : " )
                fig = plot_mimicry(give_mimicry_folder1(get_laughs_dict_conv_folder, databases_choice, 'Intensity', 
                [str.lower(intensities_laughs[0]), str.lower(intensities_laughs[1])] ))
                st.plotly_chart(fig)
                st.text("Do you want to filter by role ?")
                role_choice=st.radio(label="Choice :        ", options=["Yes", "No"])
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                if role_choice == "Yes":
                    roles=st.multiselect("Roles :       ", ["spk","lsn"])
                    for j in roles :
                        fig=plot_mimicry(give_mimicry_folder1(eval('get_laughs_from_'+j+'_folder'), databases_choice, 'Intensity', [str.lower(intensities_laughs[0]), str.lower(intensities_laughs[1])]))
                        st.write("For ",j," :")
                        st.plotly_chart(fig)
                else:
                    pass

        st.subheader('For Smiles / Laughs ')
        if st.checkbox("All intensities "):
            fig=plot_mimicry(give_mimicry_folder2(databases_choice,get_smiles_dict_conv_folder, get_laughs_dict_conv_folder))
            st.plotly_chart(fig)
            st.text("Do you want to filter by role ?")
            role_choice=st.radio(label="  Choice  :", options=["Yes", "No"])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

            if role_choice == "Yes":
                roles=st.multiselect("  Roles :", ["spk","lsn","spk / lsn"])
                for i in roles :
                    if i == "spk / lsn":
                        fig=plot_mimicry(give_mimicry_folder2(databases_choice, eval('get_smiles_from_'+i[0:3]+'_folder'), eval('get_laughs_from_'+i[-3:]+'_folder')))
                        st.write("For ",i," :")
                        st.plotly_chart(fig)
                    else:
                        fig=plot_mimicry(give_mimicry_folder2(databases_choice, eval('get_smiles_from_'+i+'_folder'), eval('get_laughs_from_'+i+'_folder')))
                        st.write("For ",i," :")
                        st.plotly_chart(fig)
            else:
                pass
        if st.checkbox("By intensity "): 
            if st.checkbox("For one intensity : "):
                intensities_laughs = st.multiselect("Intensities :", ["LOW", "MEDIUM", "HIGH"])
                for i in intensities_laughs:
                    st.write(i, "laughs mimic ", i, "smiles : " )
                    fig = plot_mimicry(give_mimicry_folder2(databases_choice,get_smiles_dict_conv_folder, get_laughs_dict_conv_folder, 
                    'Intensity', str.lower(i)))
                    st.plotly_chart(fig)
                    st.text("Do you want to filter by role ?")
                    role_choice=st.radio(label="Choice ->", options=["Yes", "No"])
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                    if role_choice == "Yes":
                        roles=st.multiselect("Roles ->", ["spk","lsn","spk / lsn"])
                        for i in roles :
                            if i == "spk / lsn":
                                fig=plot_mimicry(give_mimicry_folder2(databases_choice, eval('get_smiles_from_'+i[0:3]+'_folder'), 
                                eval('get_laughs_from_'+i[-3:]+'_folder'), 'Intensity', str.lower(i)))
                                st.write("For ",i," :")
                                st.plotly_chart(fig)
                            else:
                                fig=plot_mimicry(give_mimicry_folder2(databases_choice, eval('get_smiles_from_'+i+'_folder'), 
                                eval('get_laughs_from_'+i+'_folder'), 'Intensity', str.lower(i)))
                                st.write("For ",i," :")
                                st.plotly_chart(fig)
                    else:
                        pass
            if st.checkbox("For two intensities : "):
                intensities_laughs = st.multiselect("Intensities :", ["LOW", "MEDIUM", "HIGH"])
                st.write(intensities_laughs[1], " laughs mimic ", intensities_laughs[0], "smiles : " )
                fig = plot_mimicry(give_mimicry_folder2(databases_choice,get_smiles_dict_conv_folder, get_laughs_dict_conv_folder, 'Intensity', 
                                    [str.lower(intensities_laughs[0]), str.lower(intensities_laughs[1])] ))
                st.plotly_chart(fig)
                st.text("Do you want to filter by role ?")
                role_choice=st.radio(label="Choice -> ", options=["Yes", "No"])
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                if role_choice == "Yes":
                    roles=st.multiselect("Roles -> ", ["spk","lsn","spk / lsn"])
                    for i in roles :
                        if i == "spk / lsn":
                            fig=plot_mimicry(give_mimicry_folder2(databases_choice, eval('get_smiles_from_'+i[0:3]+'_folder'), 
                            eval('get_laughs_from_'+i[-3:]+'_folder'), 'Intensity', [str.lower(intensities_laughs[0]), str.lower(intensities_laughs[1])]))
                            st.write("For ",i," :")
                            st.plotly_chart(fig)
                        else:
                            fig=plot_mimicry(give_mimicry_folder2(databases_choice, eval('get_smiles_from_'+i+'_folder'), 
                            eval('get_laughs_from_'+i+'_folder'), 'Intensity', [str.lower(intensities_laughs[0]), str.lower(intensities_laughs[1])]))
                            st.write("For ",i," :")
                            st.plotly_chart(fig)
                else:
                    pass

        st.subheader('For Laughs / Smiles')
        if st.checkbox("All intensities  "):
            fig=plot_mimicry(give_mimicry_folder2(databases_choice, get_laughs_dict_conv_folder, get_smiles_dict_conv_folder))
            st.plotly_chart(fig)
            st.text("Do you want to filter by role ?")
            role_choice=st.radio(label="Choice ->    ", options=["Yes", "No"])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

            if role_choice == "Yes":
                roles=st.multiselect("Roles ->    ", ["spk","lsn","spk / lsn"])
                for i in roles :
                    if i == "spk / lsn":
                        fig=plot_mimicry(give_mimicry_folder2(databases_choice, eval('get_laughs_from_'+i[0:3]+'_folder'), eval('get_smiles_from_'+i[-3:]+'_folder')))
                        st.write("For ",i," :")
                        st.plotly_chart(fig)
                    else:
                        fig=plot_mimicry(give_mimicry_folder2(databases_choice, eval('get_laughs_from_'+i+'_folder'), eval('get_smiles_from_'+i+'_folder')))
                        st.write("For ",i," :")
                        st.plotly_chart(fig)
            else:
                pass   
        if st.checkbox("By intensity  "): 
            if st.checkbox("For one intensity :    "):
                intensities_laughs = st.multiselect("Intensities :", ["LOW", "MEDIUM", "HIGH"])
                for i in intensities_laughs:
                    st.write(i, "smiles mimic ", i, "laughs : " )
                    fig = plot_mimicry(give_mimicry_folder2(databases_choice, get_laughs_dict_conv_folder, get_smiles_dict_conv_folder, 
                    'Intensity', str.lower(i)))
                    st.plotly_chart(fig)
                    st.text("Do you want to filter by role ?")
                    role_choice=st.radio(label="Choice :                   ", options=["Yes", "No"])
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                    if role_choice == "Yes":
                        roles=st.multiselect("Roles :                      ", ["spk","lsn","spk / lsn"])
                        for i in roles :
                            if i == "spk / lsn":
                                fig=plot_mimicry(give_mimicry_folder2(databases_choice, eval('get_laughs_from_'+i[0:3]+'_folder'), 
                                eval('get_smiles_from_'+i[-3:]+'_folder'), 'Intensity', str.lower(i)))
                                st.write("For ",i," :")
                                st.plotly_chart(fig)
                            else:
                                fig=plot_mimicry(give_mimicry_folder2(databases_choice, eval('get_laughs_from_'+i+'_folder'), 
                                eval('get_smiles_from_'+i+'_folder'), 'Intensity', str.lower(i)))
                                st.write("For ",i," :")
                                st.plotly_chart(fig)
                    else:
                        pass
            if st.checkbox("For two intensities :   "):
                intensities_laughs = st.multiselect("Intensities :", ["LOW", "MEDIUM", "HIGH"])
                st.write(intensities_laughs[1], " smiles mimic ", intensities_laughs[0], "laughs : " )
                fig = plot_mimicry(give_mimicry_folder2(databases_choice, get_laughs_dict_conv_folder, get_smiles_dict_conv_folder, 'Intensity', 
                                    [str.lower(intensities_laughs[0]), str.lower(intensities_laughs[1])] ))
                st.plotly_chart(fig)
                st.text("Do you want to filter by role ?")
                role_choice=st.radio(label="  Choice :        ", options=["Yes", "No"])
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                if role_choice == "Yes":
                    roles=st.multiselect("  Roles :          ", ["spk","lsn","spk / lsn"])
                    for i in roles :
                        if i == "spk / lsn":
                            fig=plot_mimicry(give_mimicry_folder2(databases_choice, eval('get_laughs_from_'+i[0:3]+'_folder'), 
                            eval('get_smiles_from_'+i[-3:]+'_folder'), 'Intensity', [str.lower(intensities_laughs[0]), str.lower(intensities_laughs[1])]))
                            st.write("For ",i," :")
                            st.plotly_chart(fig)
                        else:
                            fig=plot_mimicry(give_mimicry_folder2(databases_choice, eval('get_laughs_from_'+i+'_folder'), 
                            eval('get_smiles_from_'+i+'_folder'), 'Intensity', [str.lower(intensities_laughs[0]), str.lower(intensities_laughs[1])]))
                            st.write("For ",i," :")
                            st.plotly_chart(fig)
                else:
                    pass

    def page3_3():               
        st.title('Correlation')
        st.markdown('Here, we look at the correlation between two sequences of expressions')
        st.text(" *******  By datasets  ********")

        name_databases=['CCDB','IFADV','NDC']
        databases_=[ccdb_pair, ifadv_pair, ndc_pair]
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


        st.text("********    By datasets and intensity   ********")
        databases_=[ccdb_pair, ifadv_pair, ndc_pair]
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

        #st.text("********   By datasets, role and intensity   ********")

    page3_names_to_funcs = {
        "Intra S&L effects": page3_1,
        "Inter S&L effects": page3_2,
        "Correlation": page3_3,
    }

    selected_page = st.sidebar.selectbox("Select a page", page3_names_to_funcs.keys())
    page3_names_to_funcs[selected_page]()

def page4():
    st.sidebar.markdown("ML Statistics")
    # #Barplots ______________________________________________________
    st.title('Machine Learning Statistics')
    text='''We look at the count of elements we have in input and output of our database.
    We have a few parameters to fill in before displaying the figures. 

    \nin_out (numeric): 0 if we need inputs (all person 1 in interactions of the database chosen) and 1 for outputs (all person 2 in interactions of the database chosen).
    \nn (numeric): The video number we transformed into frames. 
    \nthreshold (numeric): Value for the function which calculate how many constant and mixed lists we have in out inputs and outputs.
    
    \nNB : There are two parameters, FRAME_LEN and FRAME_TSTEP you can change in the code on ML_stats/settings.py. 
    They respectively represent the length of a frame (in ms) for one sequence and how many milliseconds the frame move.
    \nNow let's start !
    '''
    st.markdown(text)

    st.markdown('''First of all, choose the database you need.''')
    
    name_databases=['CCDB','IFADV','NDC']
    database_choice=st.radio("Expression :", name_databases)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    
    with open('..\\..\\snlstats\\SNL_Stats\\parameters.json', 'r') as f:
        parameters=json.load(f)
    PATH_IN = parameters[database_choice+"_IN_OUT"]['PATH_IN_'+database_choice]
    PATH_OUT = parameters[database_choice+"_IN_OUT"]['PATH_OUT_'+database_choice]

    st.text("Fill all the parameters.")
    in_out = st.number_input('Insert the in_out parameter.')
    if int(in_out) != 0 and int(in_out) != 1 :
        st.text("Invalid in_out. Retry.")
    in_out=int(in_out)
    st.write("n goes to 0 to ",f"{len(database_creation(PATH_IN, PATH_OUT, FRAME_LEN, FRAME_TSTEP)[in_out])-1}")
    n = st.number_input('Insert the n parameter.')
    threshold = st.number_input('Insert the threshold parameter.')
    
    def page4_1():
        if in_out==0:
            st.subheader(f"Count of elements we have in data_in[{int(n)}]")
        elif in_out==1:
            st.subheader(f"Count of elements we have in data_out[{int(n)}]")
        fig = ML_stats_viz(PATH_IN, PATH_OUT, FRAME_LEN, FRAME_TSTEP, in_out, int(n), threshold)[0]
        st.plotly_chart(fig)

    def page4_2():
        if in_out==0:
            st.subheader(f"Count of mixed and constant elements we have in data_in[{int(n)}]")
        elif in_out==1:
            st.subheader(f"Count of mixed and constant elements we have in data_out[{int(n)}]")
        fig = ML_stats_viz(PATH_IN, PATH_OUT, FRAME_LEN, FRAME_TSTEP, in_out,  int(n),threshold)[1]
        st.plotly_chart(fig)

    def page4_3():
        if in_out==0:
            st.subheader(f"Count of elements we have in constant elements in data_in[{int(n)}]")
        elif in_out==1:
            st.subheader(f"Count of elements we have in constant elements in data_out[{int(n)}]")

        fig = ML_stats_viz(PATH_IN, PATH_OUT, FRAME_LEN, FRAME_TSTEP, in_out, int(n), threshold)[2]
        st.plotly_chart(fig)

    def page4_4():
        if in_out==0:
            st.subheader(f"Count of elements we have in mixed elements in data_in[{int(n)}]")
        elif in_out==1:
            st.subheader(f"Count of elements we have in mixed elements in data_out[{int(n)}]")

        fig = ML_stats_viz(PATH_IN, PATH_OUT, FRAME_LEN, FRAME_TSTEP, in_out, int(n), threshold)[3]
        st.plotly_chart(fig)


    page4_names_to_funcs = {
        "Count of elements": page4_1,
        "Count of mixed and constant elements": page4_2,
        "Count in constant elements": page4_3,
        "Count in mixed elements": page4_4,
    }

    selected_page = st.sidebar.selectbox("Select a page", page4_names_to_funcs.keys())
    page4_names_to_funcs[selected_page]()

def page5():
    st.markdown("Here, we explore other areas to describe and see what we have in our databeses. \nLet's see each page !")
    
    def page5_1():
        st.sidebar.markdown("Expression per minute")
        # # #Barplots ______________________________________________________
        st.title('Expression per minute')
        st.markdown("We count the number of smiles or laughs we have in one minute in each database.")
        name_databases=['CCDB','IFADV','NDC']
        databases_=[ccdb_pair, ifadv_pair, ndc_pair]
        databases_choice=st.selectbox("Databases list :", name_databases)
        for i in range(len(name_databases)):
            if databases_choice==name_databases[i]:
                databases_choice=databases_[i]

        if st.checkbox("All intensities"):
            expression_choice=st.radio("Expression :", ['Smiles', 'Laughs'])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

            if expression_choice=='Smiles':
                expression_choice='Smiles_0'
            else:
                expression_choice='Laughs_0'
            choices_case=["Intra","Inter"]
            case_choice = st.radio("Case :", choices_case)
            case_list=[None, 2]
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            for _ in range (len(case_list)):
                if case_choice==choices_case[_]:
                    case_choice=case_list[_]
            st.plotly_chart(plot_expression_per_min(databases_choice, expression_choice, case_choice))

        if st.checkbox("By intensity"):
            expression_choice=st.radio("Expression : ", ['Smiles', 'Laughs'])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

            intensity_choice= st.radio("Intensity : ", ["SUBTLE", "LOW", "MEDIUM", "HIGH"])
            st.plotly_chart(plot_expression_per_min_I(databases_choice, expression_choice, str.lower(intensity_choice)))

    page5_names_to_funcs = {
        "Expression per minute": page5_1,
    }

    selected_page = st.sidebar.selectbox("Select a page", page5_names_to_funcs.keys())
    page5_names_to_funcs[selected_page]()

page_names_to_funcs = {
    "Main Page": main_page,
    "Descriptive analysis": page1,
    "S&L Analysis": page2,
    "S&L Effects": page3,
    "ML Statistics":page4,
    "Other": page5,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

