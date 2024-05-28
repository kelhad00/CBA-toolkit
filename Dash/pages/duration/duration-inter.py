from Dash.components.callbacks.dataset import get_databases_select
from Dash.components.callbacks.expression import get_expressions_select, get_expressions
from Dash.components.containers.accordion import accordion, accordion_item
from Dash.components.containers.section import section_container
from Dash.components.interaction.radio import radio
from Dash.components.interaction.select import select
from dash import html, Output, callback, Input, dcc
import dash
import dash_mantine_components as dmc

from src.page4.snl_stats_visualization_page4 import plot_inter_absolute_duration, plot_inter_relative_duration, \
    plot_inter_ad_entity1_vs_entity2_tier, plot_inter_rd_entity1_vs_entity2_tier
from src.snl_stats_extraction_data import get_parameters_tag, get_parameters

dash.register_page(
    __name__,
    path='/durations/inter',
)

layout = section_container("Inter Non Verbal Expressions Analysis", "Analysis based on each interaction between two persons. ", children=[
        dmc.Alert(
            "All figures are based on the duration of the expressions of each interaction (so two files) in the datasets.",
            title="Explanation",
            color="gray",
        ),
        accordion(
            multiple=True,
            value=["dataset", "expression"],
            children=[
            accordion_item(
                label="By dataset",
                description="Display the number of expressions per minute for all entities in the database.",
                value="dataset",
                children=[
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-durations-inter-dataset",
                        options=[]
                    ),
                    select(
                        label="Select a database",
                        multiple=True,
                        id="database-select-durations-inter-dataset",
                        options=[],
                        value=[]
                    ),
                    radio(
                        id="figure-radio-durations-inter-dataset",
                        label="Select a figure",
                        value="0",
                        options=[["0", "Scatter"], ["1", "Line"]],
                    ),
                    radio(
                        id="type-radio-durations-inter-dataset",
                        label="Select a type",
                        value="absolute",
                        options=[["absolute", "Absolute"], ["relative", "Relative"]],
                    ),
                    html.Div(className="flex flex-col gap-4", id="output-durations-dataset-inter", children=[]),
                ]
            ),
            accordion_item(
                label="Divided by expressions for a specific dataset",
                description="We are looking at the stats of a specific expression to analyse compare to another one during an interaction.",
                value="expression",
                children=[
                    select(
                        label="Select an expression (divided by)",
                        allowDeselect=True,
                        id="expression-select-durations-inter-expression-divided",
                        options=[]
                    ),
                    select(
                        label="Select an expression (analyzed)",
                        allowDeselect=True,
                        id="expression-select-durations-inter-expression-analyzed",
                        options=[]
                    ),
                    select(
                        label="Select a database",
                        allowDeselect=True,
                        id="database-select-durations-inter-expression",
                        options=[]
                    ),
                    radio(
                        id="figure-radio-durations-inter-expression",
                        label="Select a type",
                        value="absolute",
                        options=[["absolute", "Absolute"], ["relative", "Relative"]],
                    ),
                    html.Div(className="flex flex-col gap-4", id="output-durations-expression-inter", children=[]),
                ],
            ),
        ]),
    ])




@callback(
    [Output('database-select-durations-inter-dataset', 'data'), Output('database-select-durations-inter-expression', 'data')],
    Input('url', 'pathname'))
def update_database_select(pathname):
    options = get_databases_select()
    return options, options



@callback(
    [Output('expression-select-durations-inter-dataset', 'data'), Output('expression-select-durations-inter-expression-divided', 'data')],
    Input('url', 'pathname'))
def update_expression_select(pathname):
    options = get_expressions_select()

    return options, options

@callback(
    [Output('expression-select-durations-inter-expression-analyzed', 'data'), Output('expression-select-durations-inter-expression-analyzed', 'value')],
    Input('expression-select-durations-inter-expression-divided', 'value'))
def update_expression_analyzed_select(expression):
    if expression is None:
        return [], None

    name_tiers = get_expressions()

    return [{"label": tier, "value": tier} for tier in name_tiers if tier != expression], None




@callback(
    Output('output-durations-dataset-inter', 'children'),
    [Input('expression-select-durations-inter-dataset', 'value'), Input('database-select-durations-inter-dataset', 'value'), Input('figure-radio-durations-inter-dataset', 'value'), Input('type-radio-durations-inter-dataset', 'value')])
def display_durations_intra_dataset(expression, databases, type_figure, type):
    real_tier_lists, real_tiers = get_parameters_tag()

    if expression is None or databases is None:
        return None

    if real_tier_lists[expression]:
        if type == "absolute":
            figures = plot_inter_absolute_duration(databases, expression)
            return [dcc.Graph(figure=figures[i][int(type_figure)]) for i in range(len(figures)) if figures[i][int(type_figure)] is not None] or "No data available"
        else:
            figures = plot_inter_relative_duration(databases, expression)
            return [dcc.Graph(figure=figures[i][int(type_figure)]) for i in range(len(figures)) if figures[i][int(type_figure)] is not None] or "No data available"


    return "No data available"



@callback(
    Output('output-durations-expression-inter', 'children'),
    [Input('expression-select-durations-inter-expression-divided', 'value'), Input('expression-select-durations-inter-expression-analyzed', 'value'), Input('database-select-durations-inter-expression', 'value'), Input('figure-radio-durations-inter-expression', 'value')])
def display_durations_intra_expression(expression_divided, expression_analyzed, database, type):
    real_tier_lists, real_tiers = get_parameters_tag()

    if expression_divided is None or expression_analyzed is None or database is None or type is None:
        return []

    # get entity of the expressions
    entities_divided = real_tier_lists[expression_divided]['Intensities']

    print(entities_divided)

    figures = []
    for entity_divided in entities_divided:
        entities_analyzed = entities_divided
        for entity_analyzed in entities_analyzed:
            if type == "absolute":
                figure, df = plot_inter_ad_entity1_vs_entity2_tier(database, expression_divided, expression_analyzed, entity_divided, entity_analyzed)
                figures.append(dcc.Graph(figure=figure) if figure is not None else f"No data available for {entity_divided} vs {entity_analyzed} in {database}")
            else:
                figure, df = plot_inter_rd_entity1_vs_entity2_tier(database, expression_divided, expression_analyzed, entity_divided, entity_analyzed)
                figures.append(dcc.Graph(figure=figure) if figure is not None else f"No data available for {entity_divided} vs {entity_analyzed} in {database}")


    return figures




