import dash
from dash import html,dcc, callback, Output, Input
import dash_mantine_components as dmc

from app.components.callbacks.dataset import get_databases_select, get_database_paths
from app.components.callbacks.entity import get_entities
from app.components.callbacks.expression import get_expressions_select
from app.components.containers.accordion import accordion_item, accordion
from app.components.containers.page import page_container
from app.components.containers.section import section_container
from app.components.interaction.button import download_button
from app.components.interaction.radio import radio, radio_items
from app.components.interaction.select import select

from src.json_creation import create_json_from_directory
from src.description.snl_stats_visualization_page3_express import plot_expression_per_min_I, plot_expression_per_min
from src.snl_stats_extraction_data import get_parameters, get_parameters_tag

dash.register_page(
    __name__,
    path="/description/per_minute",
)


layout = section_container("Expression Per Minute", "Count the number of expressions or tiers per minutes in each dataset.", children=[
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
                        options=[
                            ["", dmc.Tooltip(children="Intra", label="we count the number of expressions/tiers we have in one minute in each file/individual.", radius="md", withArrow=True)],
                            ["2", dmc.Tooltip(children="Inter", label="we count the number of expressions/tiers we have in one minute in each interaction.", radius="md", withArrow=True)]
                        ],
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
    return get_databases_select()


@callback(
    [Output('expression-select-per-minute-all', 'data'), Output('expression-select-per-minute-entity', 'data')],
    Input('url', 'pathname'))
def update_expression_select(pathname):
    options = get_expressions_select()
    return options, options

@callback(
    [Output('entity-radio-per-minute-entity', 'children'),Output('entity-radio-per-minute-entity', 'value')],
    Input('expression-select-per-minute-entity', 'value'))
def update_entity_radio(expression):
    if expression is not None:
        entities = get_entities(expression)
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

    if database is None or expression is None or pov is None:
        return []

    database_paths = get_database_paths(database)

    fig, df = plot_expression_per_min(
        database_paths,
        expression,
        None if pov == "" else int(pov)
    )

    return [dcc.Graph(figure=fig), download_button(df.to_csv(index=False), f"{database}_{expression}_all_per_minute.csv")]


@callback(
    Output('output-per-minute-entity', 'children'),
    [Input('database-select-per-minute', 'value'),
     Input('expression-select-per-minute-entity', 'value'),
     Input('entity-radio-per-minute-entity', 'value')])
def update_output_per_minute_entity(database, expression, entity):
    if database is None or expression is None or entity is None:
        return []

    database_paths = get_database_paths(database)

    fig, df = plot_expression_per_min_I(database_paths, expression, entity)

    return [dcc.Graph(figure=fig), download_button(df.to_csv(index=False), f"{database}_{expression}_{entity}_per_minute.csv")]















