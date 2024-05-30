from src.snl_stats_extraction_data import get_parameters_tag


def get_entities(expression):
    """ Get the entities for the select component.
        Args:
           expression (str): Name of the expression.
        Returns:
            list: List of dictionaries containing the label and value of each entity.
    """
    real_tier_lists, real_tiers = get_parameters_tag()

    if expression is not None:
        return real_tier_lists[expression]['Intensities']
    else:
        return []

