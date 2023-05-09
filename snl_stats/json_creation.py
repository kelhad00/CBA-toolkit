import os 
from os.path import join, relpath
import json


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
    for d in range(len(datasets_full)):
        folder_name = datasets[d]
        temp = os.listdir(datasets_full[d])
        dct['DATABASES_PATHS'][f'{folder_name}_paths'] = [relpath(join(datasets_full[d], f), os.getcwd()) for f in temp]
    
    
    with open('data.json', 'w') as f:
        json.dump(dct, f, indent=4)

def delete_file_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)
        

root = os.path.abspath("data")
delete_file_if_exists('data.json')
create_json_from_directory(root)


