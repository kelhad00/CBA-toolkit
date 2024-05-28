from src.snl_stats_extraction_data import get_parameters_tag


def get_entities(expression):
    real_tier_lists, real_tiers = get_parameters_tag()

    if expression is not None:
        return real_tier_lists[expression]['Intensities']
    else:
        return []

