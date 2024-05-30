from src.snl_stats_extraction_data import get_parameters


def get_databases_select():
    """ Get the list of databases for the select component.
        Args:
           None
        Returns:
            list: List of dictionaries containing the label and value of each database.
    """
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    name_databases = [key.replace('_paths', '').upper() for key in databases.keys()]
    return [
        {"label": database, "value": database} for database in name_databases
    ]

def get_databases():
    """ Get the list of databases.
            Args:
               None
            Returns:
                list: List of database names.
        """
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    databases = [key.replace('_paths', '').upper() for key in databases.keys()]

    return databases

def get_database_paths(database):
    """ Get the paths of the database.
        Args:
            database (str): Name of the database.
        Returns:
            list: List of paths of the database.
    """
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    return databases_paths[database.lower() + "_paths"]