import streamlit as st
import os, sys, json
import Affichage_pattern

script_path = os.path.realpath(os.path.dirname("snl_stats"))
os.chdir(script_path)
sys.path.append("..")

Affichage_pattern.affichage()
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


main_page()