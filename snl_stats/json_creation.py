import os, sys 
from os.path import join, relpath
import json
from bs4 import BeautifulSoup
from pympi import Eaf

script_path = os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")

from IBPY import db

def create_json_from_directory(root):
    datasets = os.listdir(root)
    datasets_full = [join(root, d) for d in datasets]
    dct = {}
    
    # Ajout du sous-dictionnaire pour les FOLDER_PATHS
    dct['FOLDER_PATHS'] = {}
    dct['FOLDER_PATHS']['DIR'] = relpath(root, os.getcwd())
    for i, folder_path in enumerate(datasets_full):
        dct['FOLDER_PATHS'][f'ROOT{i+1}'] = relpath(folder_path, os.getcwd())
    
    # Ajout du sous-dictionnaire pour les DATABASES_PATHS
    dct['DATABASES_PATHS'] = {}
    dct['DATABASES_PAIR_PATHS'] = {} # nouveau sous-dictionnaire pour les pairs
    for d in range(len(datasets_full)):
        folder_name = datasets[d]
        temp = os.listdir(datasets_full[d])
        eaf_files = [f for f in temp if f.endswith('.eaf')]
        dct['DATABASES_PATHS'][f'{folder_name}_paths'] = [relpath(join(datasets_full[d], f), os.getcwd()) for f in eaf_files]
        
        # Création des pairs pour le sous-dictionnaire "DATABASES_PAIR_PATHS"
        pair_func_name = f"form_pairs_{folder_name.lower()}"
        if hasattr(db, pair_func_name):
            pair_func = getattr(db, pair_func_name)
            pair_files = []
            try:
                pair_files = pair_func(eaf_files)
            except Exception as e:
                print(f"Error while creating pairs for folder {folder_name}: {e}")
                continue
            if pair_files:
                pair_paths = []
                for f in pair_files:
                    if isinstance(f, tuple):
                        pair_paths.extend([relpath(join(str(datasets_full[d]), str(p)), os.getcwd()) for p in f])
                    else:
                        pair_paths.append(relpath(join(str(datasets_full[d]), str(f)), os.getcwd()))
                dct['DATABASES_PAIR_PATHS'][f'{folder_name}_pairs'] = pair_paths

    # Création du dictionnaire pour les tiers et les annotations
    dct['TIER_LISTS'] = {}
    for d in range(len(datasets_full)):
        temp = os.listdir(datasets_full[d])
        for f in temp:
            if f.endswith('.eaf'):
                eaf = Eaf(join(datasets_full[d], f))
                for tier_name in eaf.get_tier_names():
                    if tier_name not in dct['TIER_LISTS']:
                        dct['TIER_LISTS'][tier_name] = []
                    annotations = eaf.get_annotation_data_for_tier(tier_name)
                    for annotation in annotations:
                        value = annotation[2].strip()
                        if value and not value.isdigit() and value not in dct['TIER_LISTS'][tier_name]:
                            dct['TIER_LISTS'][tier_name].append(value)

    with open('data.json', 'w') as f:
        json.dump(dct, f, indent=4)

def delete_file_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)
        

root = os.path.abspath("data")
delete_file_if_exists('data.json')
create_json_from_directory(root)


