import streamlit as st
import os, sys, json
import Affichage_pattern
from pathlib import Path
from pyunpack import Archive
import zipfile
import shutil

script_path = os.path.realpath(os.path.dirname("src"))
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
# Fonction pour extraire le contenu d'une archive ZIP
def extract_zip(file):
     
    file_name = file.name.rstrip('zip')
    path = "../data/"+file_name
    with zipfile.ZipFile(file, "r") as zip_ref:
        
        files = zip_ref.namelist()
        eaf_files = []  

        for file in files :
            if file.endswith(".eaf") :
                eaf_files.append(file)

        if len(eaf_files) == 0 or len(eaf_files) != len(files):
            st.error("Invalid directory")
            return
    
        zip_ref.extractall('../data')

    st.success("Valid directory!")

def main_page():
    #st.markdown("# Main page")

    st.sidebar.markdown("Main page")
    st.title('Smiles and Laughs Study ')
    st.markdown('''This is an interactive web page where we are going to show some statistics based on a given database.
    \nThis database contains for the moment three datasets : CCDB, IFADV and NDC. Each dataset has files containing smiles and laughs. 
    \nWe explored these smiles and laughs and we tried to know which kind of effects they could have on a person or during an interaction.
    \n\nNow look at each page of the web page !''')
    folder = st.file_uploader("Select the folder you want to import : ", type='zip')
    if folder is not None:
        extract_zip(folder)

main_page()