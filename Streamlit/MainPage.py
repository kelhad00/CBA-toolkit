import streamlit as st
import os, sys, json
import Affichage_pattern
from pathlib import Path
from pyunpack import Archive
import zipfile
import shutil

Affichage_pattern.affichage()
script_path = os.path.realpath(os.path.dirname("src"))
os.chdir(script_path)
sys.path.append("..")

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
    """ Extract the content of a zip file in the data folder.
    
    Args:
        file (zipfile): the zip file to extract
    Returns:
        None
    """
    file_name=file.name.replace('.zip', '')
    path="../data/"
    if not os.path.exists(path):
        #Creation of the directory
        os.makedirs(path)
    with zipfile.ZipFile(file, "r") as zip_ref:
        files=zip_ref.namelist()
        only_files=[f for f in files if not zip_ref.getinfo(f).is_dir()]	
        subfolders=[f for f in files if f.endswith('/')]
        # print(len(subfolders))
        split_sulfolders=[]
        for folder in subfolders:
            split_sulfolders.append(folder.split('/')[-2])
        for folder in split_sulfolders:
            os.makedirs(path+folder, exist_ok=True)
        eaf_files=[]  
        for file in only_files:
            if file.endswith(".eaf"):
                eaf_files.append(file)
        if len(eaf_files)==0 or len(eaf_files)!=len(only_files):
            st.error("Invalid directory")
            return
        zip_ref.extractall(path)
        for folder in split_sulfolders:
            doss=os.path.join(path, file_name)
            doss2=os.path.join(doss, folder)
            for file2 in os.listdir(doss2):
                chemin_source=os.path.join(doss2, file2)
                chemin_destination=os.path.join(os.path.join(path, folder), file2)
                # Verification if the file is a file (and not a subfolder)
                if os.path.isfile(chemin_source):
                    shutil.move(chemin_source, chemin_destination)           
        if split_sulfolders:
            shutil.rmtree(os.path.join(path, file_name))
    st.success("Valid directory!")

def main_page():
    st.sidebar.markdown("Main page")
    st.title('Non Verbal Expressions Study')
    st.markdown('''This is an interactive web page where we are going to show some statistics based on a given database.''')
    
    folder=st.file_uploader('''Select the folder you want to import: ''', type='zip')
    if folder is not None:
        extract_zip(folder)

    st.markdown('''Each dataset of your database has files containing a list of tiers/expressions expressed during interactions between two people to be studied. 
    \nWe explored these tiers and we tried to know which kind of effects they could have on a person or during an interaction.
    \n\nNow look at each page of the web page!''')

main_page()