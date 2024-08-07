import dash
from dash import html, Output, callback, Input, dcc
import dash_mantine_components as dmc

from Dash.components.callbacks.dataset import get_databases
from Dash.components.callbacks.expression import get_expressions_select
from Dash.components.containers.accordion import accordion_item, accordion
from Dash.components.containers.graph import graph_container
from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container
from Dash.components.interaction.select import select
from src.effect.snl_stats_visualization_page5 import plot_track_previous_expression, plot_track_following_expression, \
    plot_track_previous_expression_byI, plot_track_following_expression_byI
from src.snl_stats_extraction_data import get_parameters_tag, get_parameters, expression_track, expression_track_byI

dash.register_page(__name__, path='/tracking/')

layout = section_container("Expressions Track", "Check what is before and after an expression in ploting percentage of the preceded and next expression for each individual", children=[
    dmc.Alert(
        "The goal is to see if there is any pattern or influence of the non verbal expressions in a same sequence while taking into account the expressions and their entities.",
        title="Explanation",
        color="gray",
    ),
    accordion(
        multiple=True,
        value=["expression", "entity"],
        children=[
        accordion_item(
            label="By expression",
            description="Display the sequence of expressions of an individual.",
            value="expression",
            children=[
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
            label="By entity",
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
    options = get_expressions_select()
    return options, options, options, options



@callback(
    Output('output-effects-intra-expression', 'children'),
    [Input('expression-select-effects-intra-expression-track', 'value'),
     Input('expression-select-effects-intra-expression-check', 'value')])
def update_output_expression(expression_tracked, expression_checked):
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()

    if expression_tracked is None or expression_checked is None:
        return []

    databases = get_databases()

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
    if previous_figure is not None:
        figures.append(graph_container(figure=previous_figure, csv=df.to_csv(index=False), name=f"{expression_tracked}_{expression_checked}_track_previous"))

    following_figure, df = plot_track_following_expression(
        expression_track(
            expression_checked,
            expression_tracked,
            DIR,
            databases
        ),
        expression_tracked
    )
    if following_figure is not None:
        figures.append(graph_container(figure=following_figure, csv=df.to_csv(index=False), name=f"{expression_tracked}_{expression_checked}_track_following"))

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

    databases = get_databases()

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
        figures.append(graph_container(figure=previous_figure, csv=df.to_csv(index=False), name=f"{expression_tracked}_{expression_checked}_track_previous"))

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
        figures.append(graph_container(figure=following_figure, csv=df.to_csv(index=False), name=f"{expression_tracked}_{expression_checked}_track_following"))

    return figures

