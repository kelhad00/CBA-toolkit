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
        split_subfolders = []
        for folder in subfolders:
            folder_path = os.path.normpath(folder) 
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
                src_path = os.path.join(doss2, file2)
                destination_path = os.path.join(os.path.join(path, folder), file2)
                # Verification if the file is a file (and not a subfolder)
                if os.path.isfile(src_path):
                    shutil.move(src_path, destination_path)           
        if split_subfolders :
            shutil.rmtree(os.path.join(path, file_name))
        dataset_name = file_name
        add_form_pairs_function(dataset_name)
    st.success("Valid directory!")

def add_form_pairs_function(dataset_name):
    relative_path = os.path.join("..", "IBPY")
    db_py_path = os.path.join(relative_path, "db.py")
    form_pairs_code = f'''
def form_pairs_{dataset_name}(lst):
    """Return filename pairs [(), (), ...].

    Args:
        lst (list): list of filenames without the path.
    Returns:
        list: [(), (), ...].
    """
    pairs = form_pairs_ab(lst)
    return pairs
'''
    # Load contents of db.py file
    with open(db_py_path, "r") as file:
        content = file.read()
    # Analyze the source code of the file
    tree = ast.parse(content)
    # Check if function already exists
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == f"form_pairs_{dataset_name}":
            #print("The function already exists.")
            return
    # Create AST for the new function
    new_tree = ast.parse(form_pairs_code)
    new_function_def = new_tree.body[0]
    new_function_def.name = f"form_pairs_{dataset_name}"
    # Add function to existing AST
    tree.body.append(new_function_def)
    # Convert the modified AST to text
    modified_code = ast.unparse(tree)
    # Write the modified code back to db.py file
    with open(db_py_path, "w") as file:
        file.write(modified_code)
    #print(f"The form_pairs_{dataset_name} function was successfully added.")


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
    st.markdown(''' ''')
    st.markdown('''-----------------------------------------------------------------------------------------------------------------''')
    st.markdown(''' ''')
    st.markdown('''Here enter your own code to explore your dataset if the way of naming the eaf files by interaction pairs is different from "A_1_..." & "B_1_..." for example.
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

                with open(filename, 'w') as file:
                    file.write(content)

                try:
                    with open(filename, 'r') as file:
                        python_code = file.read()
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
                    if is_declaration_function == True:
                        if duplicates:
                            # Remove existing function from AST
                            for node in ast.walk(tree_destination):
                                if isinstance(node, ast.FunctionDef) and node.name in duplicates:
                                    tree_destination.body.remove(node)

                        with open(target_file, 'w') as f_destination:
                            f_destination.write(ast.unparse(tree_destination))
                            f_destination.write("\n")
                            f_destination.write("\n")
                            f_destination.write(python_code)

                        os.remove(filename)
                        st.success("Code successfuly uploaded !!")
                    else:
                        os.remove(filename)
                        st.error("Your code didn't verify conditions")
                    
            except Exception as e:
                traceback.print_exc()
                st.error("Error in your code :( ")

            content = None
        else : 

            return False

main_page()