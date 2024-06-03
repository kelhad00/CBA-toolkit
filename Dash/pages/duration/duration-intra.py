import dash
from dash import html, callback, Output, Input, dcc
import dash_mantine_components as dmc

from Dash.components.callbacks.dataset import get_databases_select, get_database_paths
from Dash.components.callbacks.entity import get_entities
from Dash.components.callbacks.expression import get_expressions_select, get_expressions
from Dash.components.containers.accordion import accordion, accordion_item
from Dash.components.containers.graph import graph_container
from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container
from Dash.components.interaction.radio import radio
from Dash.components.interaction.select import select
from src.page4.snl_stats_visualization_page4 import plot_intra_absolute_duration, plot_intra_relative_duration, \
    plot_absolute_duration_from_tier_folder, plot_relative_duration_from_tier_folder
from src.snl_stats_extraction_data import get_parameters, get_parameters_tag

# from Dash.pages.duration_pages.inter import display_durations_inter
# from Dash.pages.duration_pages.intra import display_durations_intra

dash.register_page(
    __name__,
    path='/durations/intra',
)


options = [
    {"label": "Intra Non Verbal Expressions Analysis", "value": "/durations/intra"},
    {"label": "Inter Non Verbal Expressions Analysis", "value": "/durations/inter"},
]


layout = section_container("Intra Non Verbal Expressions Analysis", "Analysis based on each individual.", children=[
        dmc.Alert(
            "We look here at the sequence of expressions of each individual in each .eaf file of the datasets. All figures are based on the duration of the expressions of each individual in the datasets.",
            title="Explanation",
            color="gray",
        ),
        accordion(
            multiple=True,
            value=["dataset", "expression"],
            children=[
            accordion_item(
                label="By dataset",
                description="Display the durations of a given expression in the selected databases.",
                value="dataset",
                children=[
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-durations-intra-dataset",
                        options=[]
                    ),
                    select(
                        label="Select a database",
                        multiple=True,
                        id="database-select-durations-intra-dataset",
                        options=[],
                        value=[]
                    ),
                    radio(
                        id="figure-radio-durations-intra-dataset",
                        label="Select a figure",
                        value="0",
                        options=[["0", "Scatter"], ["1", "Line"]],
                    ),
                    radio(
                        id="type-radio-durations-intra-dataset",
                        label="Select a type",
                        value="absolute",
                        options=[
                            ["absolute", dmc.Tooltip(children="Absolute",
                                                     label="The sum of all difference of time over the entire video",
                                                     radius="md", withArrow=True)],
                            ["relative", dmc.Tooltip(children="Absolute",
                                                     label="The percentage of the absolute duration compared to the total duration of the video.",
                                                     radius="md", withArrow=True)],
                        ],
                    ),
                    html.Div(className="flex flex-col gap-4", id="output-durations-dataset-intra", children=[]),
                ]
            ),
            accordion_item(
                label="Divided by expressions for a specific dataset",
                description="Display the durations of a specific expression divided by another expression in the selected databases.",
                value="expression",
                children=[
                    select(
                        label="Select an expression (divided by)",
                        allowDeselect=True,
                        id="expression-select-durations-intra-expression-divided",
                        options=[]
                    ),
                    select(
                        label="Select an expression (analyzed)",
                        allowDeselect=True,
                        id="expression-select-durations-intra-expression-analyzed",
                        options=[]
                    ),
                    select(
                        label="Select a database",
                        allowDeselect=True,
                        id="database-select-durations-intra-expression",
                        options=[]
                    ),
                    radio(
                        id="figure-radio-durations-intra-expression",
                        label="Select a type",
                        value="absolute",
                        options=[
                            ["absolute", dmc.Tooltip(children="Absolute",
                                                     label="The sum of all difference of time over the entire video",
                                                     radius="md", withArrow=True)],
                            ["relative", dmc.Tooltip(children="Absolute",
                                                     label="The percentage of the absolute duration compared to the total duration of the video.",
                                                     radius="md", withArrow=True)],
                        ],
                    ),
                    html.Div(className="flex flex-col gap-4", id="output-durations-expression-intra", children=[]),
                ],
            ),
        ]),
    ])



@callback(
    [Output('database-select-durations-intra-dataset', 'data'), Output('database-select-durations-intra-expression', 'data')],
    Input('url', 'pathname'))
def update_database_select(pathname):
    options = get_databases_select()

    return options, options



@callback(
    [Output('expression-select-durations-intra-dataset', 'data'), Output('expression-select-durations-intra-expression-divided', 'data')],
    Input('url', 'pathname'))
def update_expression_select(pathname):
    options = get_expressions_select()
    return options, options

@callback(
    [Output('expression-select-durations-intra-expression-analyzed', 'data'), Output('expression-select-durations-intra-expression-analyzed', 'value')],
    Input('expression-select-durations-intra-expression-divided', 'value'))
def update_expression_analyzed_select(expression):
    if expression is None:
        return [], None

    name_tiers = get_expressions()

    return [{"label": tier, "value": tier} for tier in name_tiers if tier != expression], None

@callback(
    Output('output-durations-dataset-intra', 'children'),
    [Input('expression-select-durations-intra-dataset', 'value'), Input('database-select-durations-intra-dataset', 'value'), Input('figure-radio-durations-intra-dataset', 'value'), Input('type-radio-durations-intra-dataset', 'value')])
def display_durations_intra_dataset(expression, databases, type_figure, type):
    real_tier_lists, real_tiers = get_parameters_tag()

    if expression is None or databases is None:
        return None

    if real_tier_lists[expression]:
        if type == "absolute":
            figures = plot_intra_absolute_duration(databases, expression)
            return [graph_container(figure=figures[i][int(type_figure)], csv=figures[i][2].to_csv(index=False), name=f"{databases}_{i}_{expression}_duration_intra") for i in range(len(figures)) if figures[i][int(type_figure)] is not None] or "No data available"
        else:
            figures = plot_intra_relative_duration(databases, expression)
            return [graph_container(figure=figures[i][int(type_figure)], csv=figures[i][2].to_csv(index=False), name=f"{databases}_{i}_{expression}_duration_intra") for i in range(len(figures)) if figures[i][int(type_figure)] is not None] or "No data available"


    return "No data available"


@callback(
    Output('output-durations-expression-intra', 'children'),
    [Input('expression-select-durations-intra-expression-divided', 'value'), Input('expression-select-durations-intra-expression-analyzed', 'value'), Input('database-select-durations-intra-expression', 'value'), Input('figure-radio-durations-intra-expression', 'value')])
def display_durations_intra_expression(expression_divided, expression_analyzed, database, type):

    if expression_divided is None or expression_analyzed is None or database is None or type is None:
        return []

    database_paths = get_database_paths(database)
    expression_values = get_entities(expression_divided)

    figures = []
    for entity in expression_values:
        if type == "absolute":
            figure, df = plot_absolute_duration_from_tier_folder(
                database_paths,
                database,
                expression_divided,
                expression_analyzed,
                entity
            )
            figures.append((figure, df))
        else:
            figure, df = plot_relative_duration_from_tier_folder(
                database_paths,
                database,
                expression_divided,
                expression_analyzed,
                entity
            )
            figures.append((figure, df))

    return [graph_container(figure=figures[i][0], csv=figures[i][1].to_csv(index=False), name=f"{database}_{expression_divided}_{expression_analyzed}_duration_intra.csv") for i in range(len(figures)) if figures[i][0] is not None] or "No data available"















