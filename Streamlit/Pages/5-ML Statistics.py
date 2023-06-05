import subprocess
import streamlit as st
import os, sys, json
import Affichage_pattern

Affichage_pattern.affichage()
script_path = os.path.realpath(os.path.dirname("src"))
os.chdir(script_path)
sys.path.append("..")

from src.ml_stats import *
from src.ml_stats_vizualisation import *
from src.settings import *
from src.snl_stats_extraction_data import get_parameters
DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()

def page4():
    st.sidebar.markdown("ML Statistics")
    # #Barplots ______________________________________________________
    st.title('Machine Learning Statistics')
    text='''We look at the count of elements we have in input and output of our database.
    We have a few parameters to fill in before displaying the figures. 

    \nin_out (numeric): 0 if we need inputs (all person 1 in interactions of the database chosen) and 1 for outputs (all person 2 in interactions of the database chosen).
    \nn (numeric): The video number we transformed into frames. 
    \nthreshold (numeric): Value for the function which calculate how many constant and mixed lists we have in out inputs and outputs.
    
    \nNB : There are two parameters, FRAME_LEN and FRAME_TSTEP you can change in the code on interaction_stats/settings.py. 
    They respectively represent the length of a frame (in ms) for one sequence and how many milliseconds the frame move.
    \nNow let's start !
    '''
    st.markdown(text)

    st.markdown('''First of all, choose the database you need.''')
    
    name_databases = [key.rstrip('_paths').upper() for key in databases.keys()]
    database_choice=st.radio("Dataset choice:", name_databases)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    update = "Still in progress..."
    
    if update is None :
        with open('..\\..\\CBA-toolkit\\snl_stats\\parameters.json', 'r') as f:
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
    
    else :
        st.text(update)

subprocess.run(["python", "..\\src\\snl_stats_extraction_data.py"])
page4()