from src.snl_stats_extraction_data import get_parameters_tag


def get_expressions_select():
    """ Get the list of expressions for the select component.
        Args:
           None
        Returns:
            list: List of dictionaries containing the label and value of each expression.
    """
    real_tier_lists, real_tiers = get_parameters_tag()

    lst_tiers_choice = []
    for tier in real_tier_lists.keys():
        if real_tier_lists[tier]['Intensities'] is not None or real_tier_lists[tier]['Replace_Value'] != "":
            lst_tiers_choice.append(tier)

    return [
        {"label": tier, "value": tier} for tier in lst_tiers_choice
    ]


def get_expressions():
    """ Get the list of expressions.
            Args:
               None
            Returns:
                list: List of expression names.
        """
    real_tier_lists, real_tiers = get_parameters_tag()

    lst_tiers_choice = []
    for tier in real_tier_lists.keys():
        if real_tier_lists[tier]['Intensities'] is not None or real_tier_lists[tier]['Replace_Value'] != "":
            lst_tiers_choice.append(tier)

    return lst_tiers_choice
