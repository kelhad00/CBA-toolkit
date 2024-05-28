from src.snl_stats_extraction_data import get_parameters


def get_databases_select():
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    name_databases = [key.replace('_paths', '').upper() for key in databases.keys()]
    return [
        {"label": database, "value": database} for database in name_databases
    ]

def get_databases():
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    databases = [key.replace('_paths', '').upper() for key in databases.keys()]

    return databases

def get_database_paths(database):
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    return databases_paths[database.lower() + "_paths"]