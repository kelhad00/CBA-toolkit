import dash
from dash import html,dcc, callback, Output, Input
import dash_mantine_components as dmc

from Dash.components.containers.accordion import accordion_item, accordion
from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container
from Dash.components.interaction.radio import radio, radio_items
from Dash.components.interaction.select import select

from src.json_creation import create_json_from_directory
from src.page3.snl_stats_visualization_page3_express import plot_expression_per_min_I, plot_expression_per_min
from src.snl_stats_extraction_data import get_parameters, get_parameters_tag

dash.register_page(
    __name__,
    path="/description/per_minute",
)


layout = section_container("Expression Per Minute", "We count the number of expressions/tiers we have in one minute in each dataset.", children=[
        select(
            label="Select a database",
            allowDeselect=True,
            id="database-select-per-minute",
            options=[]
        ),
        accordion(
            multiple=True,
            value=["all", "entity"],
            children=[
            accordion_item(
                label="All entities",
                description="Display the number of expressions per minute for all entities in the database.",
                value="all",
                children=[
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-per-minute-all",
                        options=[]
                    ),
                    radio(
                        id="pov-radio-per-minute-all",
                        label="Select a point of view",
                        value="",
                        options=[["", "Intra"], ["2", "Inter"]],
                    ),
                    html.Div(className="flex flex-col gap-4", id="output-per-minute-all", children=[]),
                ]
            ),
            accordion_item(
                label="By entity",
                description="Display the number of expressions per minute by entity in the database.",
                value="entity",
                children=[
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-per-minute-entity",
                        options=[]
                    ),
                    radio(
                        id="entity-radio-per-minute-entity",
                        label="Select an entity",
                        options=[],
                    ),
                    html.Div(className="flex flex-col gap-4", id="output-per-minute-entity", children=[]),

                ],
            ),
        ]),
    ])



@callback(
    Output('database-select-per-minute', 'data'),
    Input('url', 'pathname'))
def update_database_select(pathname):
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    name_databases = [key.replace('_paths', '').upper() for key in databases.keys()]
    return [
        {"label": database, "value": database} for database in name_databases
    ]


@callback(
    [Output('expression-select-per-minute-all', 'data'), Output('expression-select-per-minute-entity', 'data')],
    Input('url', 'pathname'))
def update_expression_select(pathname):
    real_tier_lists, real_tiers = get_parameters_tag()
    lst_tiers_choice = []

    for tier in real_tier_lists.keys():
        if real_tier_lists[tier]['Intensities'] != None or real_tier_lists[tier]['Replace_Value'] != "":
            lst_tiers_choice.append(tier)

    name_tiers = lst_tiers_choice

    tiers_data = [{"label": tier, "value": tier} for tier in name_tiers]

    return tiers_data, tiers_data

@callback(
    [Output('entity-radio-per-minute-entity', 'children'),Output('entity-radio-per-minute-entity', 'value')],
    Input('expression-select-per-minute-entity', 'value'))
def update_entity_radio(expression):
    real_tier_lists, real_tiers = get_parameters_tag()

    if expression is not None:
        entities = real_tier_lists[expression]['Intensities']
        if len(entities) > 0:
            return radio_items([[entity, entity] for entity in entities]), entities[0]
        else:
            return radio_items([]), None
    else:
        return radio_items([]), None



@callback(
    Output('output-per-minute-all', 'children'),
    [Input('database-select-per-minute', 'value'),
     Input('expression-select-per-minute-all', 'value'),
     Input('pov-radio-per-minute-all', 'value')])
def update_output_per_minute_all(database, expression, pov):
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()

    if database is None or expression is None:
        return []

    if pov == "":
        pov = None
    elif pov == "2":
        pov = 2

    database_paths = databases_paths[database.lower() + "_paths"]


    fig, df3 = plot_expression_per_min(database_paths, expression, pov)

    return dcc.Graph(figure=fig)


@callback(
    Output('output-per-minute-entity', 'children'),
    [Input('database-select-per-minute', 'value'),
     Input('expression-select-per-minute-entity', 'value'),
     Input('entity-radio-per-minute-entity', 'value')])
def update_output_per_minute_entity(database, expression, entity):
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()

    if database is None or expression is None or entity is None:
        return []

    database_paths = databases_paths[database.lower() + "_paths"]

    print(database_paths, expression, entity)

    fig, df4 = plot_expression_per_min_I(database_paths, expression, entity)

    print(fig is None)

    return dcc.Graph(figure=fig)















