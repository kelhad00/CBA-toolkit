import dash
from dash import html, Output, callback, Input, dcc
import dash_mantine_components as dmc

from Dash.components.containers.accordion import accordion_item, accordion
from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container
from Dash.components.interaction.select import select
from src.page5.snl_stats_visualization_page5 import plot_track_previous_expression, plot_track_following_expression, \
    plot_track_previous_expression_byI, plot_track_following_expression_byI
from src.snl_stats_extraction_data import get_parameters_tag, get_parameters, expression_track, expression_track_byI

dash.register_page(__name__, path='/expression/')

layout = section_container("Intra Non Verbal Expressions Effects", "", children=[
    accordion(
        multiple=True,
        value=["expression", "entity"],
        children=[
        accordion_item(
            label="Expressions Track",
            description="Check what is before and after an expression in ploting percentage of the preceded and next expression for each individual",
            value="expression",
            children=[
                dmc.Alert(
                    "We look at the sequence of expressions of an individual in order to see if there is any pattern or influence of the expressions in a same sequence.",
                    title="Explanation",
                    color="gray",
                ),
                select(
                    label="Select an expression (to check)",
                    allowDeselect=True,
                    id="expression-select-effects-intra-expression-track",
                    options=[]
                ),
                select(
                    label="Select an expression (to track)",
                    allowDeselect=True,
                    id="expression-select-effects-intra-expression-check",
                    options=[]
                ),
                html.Div(className="flex flex-col gap-4", id="output-effects-intra-expression", children=[]),
            ]
        ),
        accordion_item(
            label="Expressions Track By Entity",
            description="Same action but taking into account the entities of the expressions.",
            value="entity",
            children=[
                select(
                    label="Select an expression (to track)",
                    allowDeselect=True,
                    id="expression-select-effects-intra-entity-track",
                    options=[]
                ),
                select(
                    label="Select an expression (to check)",
                    allowDeselect=True,
                    id="expression-select-effects-intra-entity-check",
                    options=[]
                ),
                html.Div(className="flex flex-col gap-4", id="output-effects-intra-entity", children=[]),
            ],
        ),
    ]),
])


@callback(
    [Output('expression-select-effects-intra-expression-track', 'data'), Output('expression-select-effects-intra-expression-check', 'data'), Output('expression-select-effects-intra-entity-track', 'data'), Output('expression-select-effects-intra-entity-check', 'data')],
    Input('url', 'pathname'))
def update_expression_select(pathname):
    real_tier_lists, real_tiers = get_parameters_tag()

    lst_tiers_choice = []
    for tier in real_tier_lists.keys():
        if real_tier_lists[tier]['Intensities'] is not None or real_tier_lists[tier]['Replace_Value'] != "":
            lst_tiers_choice.append(tier)

    name_tiers = [
        {"label": tier, "value": tier} for tier in lst_tiers_choice
    ]

    return name_tiers, name_tiers, name_tiers, name_tiers


@callback(
    Output('output-effects-intra-expression', 'children'),
    [Input('expression-select-effects-intra-expression-track', 'value'),
     Input('expression-select-effects-intra-expression-check', 'value')])
def update_output_expression(expression_tracked, expression_checked):
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()

    if expression_tracked is None or expression_checked is None:
        return []

    databases = [key.replace('_paths', '').upper() for key in databases.keys()]

    figures = []
    previous_figure, df = plot_track_previous_expression(
        expression_track(
            expression_checked,
            expression_tracked,
            DIR,
            databases
        ),
        expression_tracked
    )
    print("prev", previous_figure)
    if previous_figure is not None:
        figures.append(dcc.Graph(figure=previous_figure))

    following_figure, df = plot_track_following_expression(
        expression_track(
            expression_checked,
            expression_tracked,
            DIR,
            databases
        ),
        expression_tracked
    )
    print("following ", following_figure)
    if following_figure is not None:
        figures.append(dcc.Graph(figure=following_figure))

    return figures


@callback(
    Output('output-effects-intra-entity', 'children'),
    [Input('expression-select-effects-intra-entity-track', 'value'),
     Input('expression-select-effects-intra-entity-check', 'value')])
def update_output_entity(expression_tracked, expression_checked):
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    real_tier_lists, real_tiers = get_parameters_tag()

    if expression_tracked is None or expression_checked is None:
        return []

    databases = [key.replace('_paths', '').upper() for key in databases.keys()]

    figures = []

    previous_figure, df= plot_track_previous_expression_byI(
        expression_track_byI(
            expression_checked,
            expression_tracked,
            DIR,
            databases,
            real_tier_lists
        )[0],
        expression_tracked,
        expression_checked,
    )
    if previous_figure is not None:
        figures.append(dcc.Graph(figure=previous_figure))

    following_figure, df = plot_track_following_expression_byI(
        expression_track_byI(
            expression_checked,
            expression_tracked,
            DIR,
            databases,
            real_tier_lists
        )[1],
        expression_tracked,
        expression_checked,
    )
    if following_figure is not None:
        figures.append(dcc.Graph(figure=following_figure))

    return figures

