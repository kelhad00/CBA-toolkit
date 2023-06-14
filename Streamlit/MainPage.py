import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
import os, sys, json
import Affichage_pattern
from pathlib import Path
from pyunpack import Archive
import zipfile
import shutil
import traceback
import ast
import re

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
    """Extract the content of a zip file in the data folder''
    Args:
        file (zipfile): the zip file to extract
    Returns:
        None
    """
    file_name = file.name.replace('.zip','')
    relative_path = os.path.join("..", "data")
    path = os.path.abspath(relative_path)
    if not os.path.exists(path):
        # Creation of the directory
        os.makedirs(path)
    with zipfile.ZipFile(file, "r") as zip_ref :
        files = zip_ref.namelist()
        only_files = [f for f in files if not zip_ref.getinfo(f).is_dir()]	
        subfolders = [f for f in files if os.path.isdir(f)]
        print(len(subfolders))
        split_subfolders = []
        for folder in subfolders:
            folder_path = os.path.normpath(folder)  # Normaliser le chemin d'accès
            split_subfolders.append(os.path.split(folder_path)[-1])
        for folder in split_subfolders:
            os.makedirs(os.path.join(path, folder), exist_ok=True)
        eaf_files = []  
        for file in only_files :
            if file.endswith(".eaf") :
                eaf_files.append(file)
        if len(eaf_files) == 0 or len(eaf_files) != len(only_files):
            st.error("Invalid directory")
            return
        zip_ref.extractall(path)
        for folder in split_subfolders:
            doss = os.path.join(path, file_name)
            doss2 = os.path.join(doss, folder)
            for file2 in os.listdir(doss2):
                chemin_source = os.path.join(doss2, file2)
                chemin_destination = os.path.join(os.path.join(path, folder), file2)
                # Verification if the file is a file (and not a subfolder)
                if os.path.isfile(chemin_source):
                    shutil.move(chemin_source, chemin_destination)           
        if split_subfolders :
            shutil.rmtree(os.path.join(path, file_name))
    st.success("Valid directory!")

def main_page():
    
    st.sidebar.markdown("Main page")
    st.title('Non Verbal Expressions Study')
    st.markdown('''This is an interactive web page where we are going to show some statistics based on a given database.''')
    
    folder = st.file_uploader('''Select the folder you want to import: ''', type='zip')
    if folder is not None:
        extract_zip(folder)

    st.markdown('''Each dataset of your database has files containing a list of tiers/expressions expressed during interactions between two people to be studied. 
    \nWe explored these tiers and we tried to know which kind of effects they could have on a person or during an interaction.
    \n\nNow look at each page of the web page!
    ''')
    st.markdown('')
    st.markdown('')
    st.markdown('''Here enter your own code to explore your database.
    \nYou will use these functions to explore your database with "foldername" the name of the dataset you want to explore:
    \n- form_pairs_foldername: to form pairs of expressions.
    \nFor more informations, please read the README.md file.
    ''')
    if 'cnt' not in st.session_state:
        st.session_state.cnt = 0
    content = st_ace(language='python', keybinding="vscode", theme='dracula')
    st.session_state.cnt += 1
    
    if content:
        if st.session_state.cnt > 1:
            try:
                exec(content)
                pattern_fonction_verifie = r"form_pairs_.*"
                filename = "temp.py"
                relative_path = os.path.join("..", "IBPY")
                relative_path = os.path.join(relative_path, "db.py")
                target_file = os.path.abspath(relative_path)

                with open(filename, 'w') as fichier:
                    fichier.write(content)

                try:
                    with open(filename, 'r') as fichier:
                        python_code = fichier.read()
                        tree = ast.parse(python_code)

                    with open(target_file, 'r') as f_destination:
                        code_destination = f_destination.read()
                        tree_destination = ast.parse(code_destination)

                except IOError:
                    tree = None
                    os.remove(filename)

                except SyntaxError:
                    tree = None
                    os.remove(filename)

                    # Checking if a function declaration is present
                if tree:
                    is_declaration_function = any((isinstance(noeud, ast.FunctionDef) and re.match(pattern_fonction_verifie, noeud.name) for noeud in ast.walk(tree)))
                    functions_source = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                    functions_destination = [node.name for node in ast.walk(tree_destination) if isinstance(node, ast.FunctionDef)]
                    duplicates = set(functions_source) & set(functions_destination)
                    if is_declaration_function == True and not duplicates :
                        with open(target_file, 'a') as f_destination:
                            f_destination.write('\n')  # Add an empty line
                            f_destination.write(python_code)
                        os.remove(filename)
                        st.success("Code successfuly uploaded !!")
                    else:
                        os.remove(filename)
                        st.error("Your code didn't verify conditions")
                    
            except Exception as e:
                traceback.print_exc()
                st.error("Error in your code :( ")
                
            content = False
        else : 

            return False

main_page()