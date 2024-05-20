import dash
from dash import html, callback, Output, Input

from Dash.components.containers.accordion import accordion, accordion_item
from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container
from Dash.components.interaction.radio import radio
from Dash.components.interaction.select import select
from src.snl_stats_extraction_data import get_parameters

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


layout = section_container("Intra Non Verbal Expressions Analysis", "It's an analysis based on each individual. We look here at the sequence of expressions of each individual in each eaf file of the datasets.", children=[
        accordion(
            multiple=True,
            value=["dataset", "expression"],
            children=[
            accordion_item(
                label="By dataset",
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
                        options=[[None, "Scatter"], [2, "Line"]],
                    ),
                    radio(
                        id="type-radio-durations-intra-dataset",
                        label="Select a type",
                        options=[[None, "Absolute"], [2, "Relative"]],
                    ),
                    html.Div(className="flex flex-col gap-4", id="output-durations-dataset-intra", children=[]),
                ]
            ),
            accordion_item(
                label="Divided by expressions for a specific dataset",
                value="expression",
                children=[
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-durations-intra-expression",
                        options=[]
                    ),
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-durations-intra-expression",
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
                        label="Select an figure",
                        options=[[None, "Scatter"], [2, "Line"]],
                    ),
                    html.Div(className="flex flex-col gap-4", id="output-durations-expression-intra", children=[]),
                ],
            ),
        ]),
    ])



@callback(
    Output('database-select-durations-intra-dataset', 'data'),
    Input('url', 'pathname'))
def update_database_select(pathname):
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    name_databases = [key.replace('_paths', '').upper() for key in databases.keys()]
    return [
        {"label": database, "value": database} for database in name_databases
    ]







