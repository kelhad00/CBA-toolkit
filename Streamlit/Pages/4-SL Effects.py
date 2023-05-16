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
from src.snl_stats_visualization import *



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
        databases_=[databases_pair_paths["ccdb_pairs"], databases_pair_paths["ifadv_pairs"], databases_pair_paths["ndc_pairs"]]
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


        st.text("********    By datasets and intensity   ********")
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

        #st.text("********   By datasets, role and intensity   ********")

    page3_names_to_funcs = {
        "Intra S&L effects": page3_1,
        "Inter S&L effects": page3_2,
        "Correlation": page3_3,
    }

    selected_page = st.sidebar.selectbox("Select a page", page3_names_to_funcs.keys())
    page3_names_to_funcs[selected_page]()

page3()