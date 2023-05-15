#Importations__________________________________________________________________________________
import os, sys, json
#script_path = os.path.realpath(os.path.dirname("_name_of_the_directory_you_need_to_access"))
#os.chdir(script_path)
#sys.path.append("..")

def tests():
    with open('..\\..\\CBA-toolkit\\src\\data.json', 'r') as f:
        parameters=json.load(f)

    DIR=parameters["FOLDER_PATHS"]["DIR"]
    databases_pair_paths = parameters["DATABASES_PAIR_PATHS"]
    databases_paths = parameters["DATABASES_PATHS"]
    tier_lists = parameters["TIER_LISTS"]

    # Parcours des jeux de données pair
    for db_name, db_path in databases_pair_paths.items():
        globals()[db_name] = db_path

    # Parcours des jeux de données
    for db_name, db_path in databases_paths.items():
        globals()[db_name] = db_path

    # Parcours des tiers d'expressions
    for tier_name, tier_list in tier_lists.items():
        globals()[f"intensity_{tier_name.lower()}"] = tier_list
    return DIR, databases_pair_paths, databases_paths, tier_lists

tests()
