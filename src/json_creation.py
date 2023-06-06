import os, sys 
from os.path import join, relpath, abspath, dirname
import json
from bs4 import BeautifulSoup
from pympi import Eaf
script_path=os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")
from IBPY.extract_data import *

# Set the script path and add it to the system path
script_path=os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")

# Import the db module from the IBPY package
from IBPY import db

def create_json_from_directory():
    """ Creates a JSON file containing information about a directory of ELAN files.

    Args:
        None
    Returns:
        None
    """
    script_dir=dirname(os.path.abspath(__file__))
    root=os.path.abspath(os.path.join(script_dir, '..', 'data'))
    delete_file_if_exists('data.json')
    parent_path=abspath(os.path.join(script_dir, '..'))
    datasets=os.listdir(root)
    datasets_full=[join(root, d) for d in datasets]
    dct={}
    dct['FOLDER_PATHS']={}
    dct['FOLDER_PATHS']['DIR']=join('..', relpath(relpath(root, os.getcwd()), parent_path))
    for i, folder_path in enumerate(datasets_full):
        dct['FOLDER_PATHS'][f'ROOT{i+1}']=join('..', relpath(relpath(folder_path, os.getcwd()), parent_path))
    # Add a sub-dictionary for the database paths
    dct['DATABASES_PATHS']={}
    dct['DATABASES_PAIR_PATHS']={} 
    for d in range(len(datasets_full)):
        folder_name=datasets[d]
        temp=os.listdir(datasets_full[d])
        eaf_files=[f for f in temp if f.endswith('.eaf')]
        dct['DATABASES_PATHS'][f'{folder_name}_paths']=[join('..', relpath(relpath(join(datasets_full[d], f), os.getcwd()), parent_path)) for f in eaf_files]
        # Create pairs for the "DATABASES_PAIR_PATHS" sub-dictionary
        pair_func_name=f"form_pairs_{folder_name.lower()}"
        if hasattr(db, pair_func_name):
            pair_func=getattr(db, pair_func_name)
            pair_files=[]
            try:
                pair_files=pair_func(eaf_files)
            except Exception as e:
                print(f"Error while creating pairs for folder {folder_name}: {e}")
                continue
            if pair_files:
                pair_paths=[]
                for f in pair_files:
                    if isinstance(f, tuple):
                        pair_paths.extend([join('..', relpath(relpath(join(str(datasets_full[d]), str(p)), os.getcwd()), parent_path)) for p in f])
                    else:
                        pair_paths.append(join('..', relpath(relpath(join(str(datasets_full[d]), str(f)), os.getcwd()), parent_path)))
                dct['DATABASES_PAIR_PATHS'][f'{folder_name}_pairs']=pair_paths
    # Create a dictionary for the tiers and annotations
    dct['TIER_LISTS']={}
    for d in range(len(datasets_full)):
        temp=os.listdir(datasets_full[d])
        for f in temp:
            if f.endswith('.eaf'):
                filepath=join(datasets_full[d], f)
                tier_dict=read_eaf_to_dict(filepath) 
                for tier_name, annotations in tier_dict.items():
                    if tier_name not in dct['TIER_LISTS']:
                        dct['TIER_LISTS'][tier_name]=[]
                    for annotation in annotations:
                        value=annotation[2].strip()
                        if isinstance(value, str) and value and not value.isspace() and not value.isdigit() and value not in dct['TIER_LISTS'][tier_name]:
                            dct['TIER_LISTS'][tier_name].append(value)
    # TO IMPROVE
    # Create a dictionary for the ML stats : IN_OUT

    # Write the data to a JSON file
    with open('data.json', 'w') as f:
        json.dump(dct, f, indent=4)


def delete_file_if_exists(filename):
    """ Deletes a file if it exists.

    Args:
        filename (str): The path of the file to delete.
    Returns:
        None
    """
    if os.path.exists(filename):
        os.remove(filename)
        
# create_json_from_directory()


