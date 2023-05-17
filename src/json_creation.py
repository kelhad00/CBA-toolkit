import os, sys 
from os.path import join, relpath, abspath, dirname
import json
from bs4 import BeautifulSoup
from pympi import Eaf

# Set the script path and add it to the system path
script_path = os.path.realpath(os.path.dirname("IBPY"))
os.chdir(script_path)
sys.path.append("..")

# Import the db module from the IBPY package
from IBPY import db

def create_json_from_directory():
    """Creates a JSON file containing information about a directory of ELAN files.

    Args:
        None

    Returns:
        None
    """

    # Absolute path of the "data" directory
    script_dir = dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(script_dir, '..', 'data'))

    # Deletes any existing "data.json" file
    delete_file_if_exists('data.json')

    # Specify the relative path to the parent folder from the script directory
    parent_path = abspath(os.path.join(script_dir, '..'))

    # Get a list of directories in the root directory
    datasets = os.listdir(root)

    # Create a list of the full paths to the directories
    datasets_full = [join(root, d) for d in datasets]

    # Create an empty dictionary to store the data
    dct = {}
    
    # Add a sub-dictionary for the folder paths
    dct['FOLDER_PATHS'] = {}
    dct['FOLDER_PATHS']['DIR'] = join('..', relpath(relpath(root, os.getcwd()), parent_path))
    for i, folder_path in enumerate(datasets_full):
        dct['FOLDER_PATHS'][f'ROOT{i+1}'] = join('..', relpath(relpath(folder_path, os.getcwd()), parent_path))
    
    # Add a sub-dictionary for the database paths
    dct['DATABASES_PATHS'] = {}
    dct['DATABASES_PAIR_PATHS'] = {} # new sub-dictionary for pairs
    for d in range(len(datasets_full)):
        folder_name = datasets[d]
        temp = os.listdir(datasets_full[d])
        eaf_files = [f for f in temp if f.endswith('.eaf')]
        dct['DATABASES_PATHS'][f'{folder_name}_paths'] = [join('..', relpath(relpath(join(datasets_full[d], f), os.getcwd()), parent_path)) for f in eaf_files]
        
        # Create pairs for the "DATABASES_PAIR_PATHS" sub-dictionary
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
                        pair_paths.extend([join('..', relpath(relpath(join(str(datasets_full[d]), str(p)), os.getcwd()), parent_path)) for p in f])
                    else:
                        pair_paths.append(join('..', relpath(relpath(join(str(datasets_full[d]), str(f)), os.getcwd()), parent_path)))
                dct['DATABASES_PAIR_PATHS'][f'{folder_name}_pairs'] = pair_paths

    # Create a dictionary for the tiers and annotations
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

                    # Remove empty tiers because they are useless        
                    if not dct['TIER_LISTS'][tier_name]:  # Check if the tier list is empty
                        del dct['TIER_LISTS'][tier_name]  # Exclude the tier from the dictionary

    # TO IMPROVE
    # Create a dictionary for the ML stats : IN_OUT

    # Write the data to a JSON file
    with open('data.json', 'w') as f:
        json.dump(dct, f, indent=4)


def delete_file_if_exists(filename):
    """Deletes a file if it exists.

    Args:
        filename (str): The path of the file to delete.

    Returns:
        None
    """
    if os.path.exists(filename):
        os.remove(filename)
        
# create_json_from_directory()


