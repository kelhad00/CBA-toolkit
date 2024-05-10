from dash import html, dcc, callback, Output, Input
from src.snl_stats_extraction_data import get_parameters, get_parameters_tag

DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
real_tier_lists , real_tiers = get_parameters_tag()


def display_general_informations(database):
    return html.Div(str(tiers))