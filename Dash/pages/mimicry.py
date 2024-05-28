import dash
from dash import html, Output, callback, Input, dcc
import dash_mantine_components as dmc

from Dash.components.callbacks.dataset import get_databases_select, get_database_paths
from Dash.components.callbacks.entity import get_entities
from Dash.components.callbacks.expression import get_expressions_select, get_expressions
from Dash.components.containers.accordion import accordion_item, accordion
from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container
from Dash.components.interaction.radio import radio, radio_items
from Dash.components.interaction.select import select
from IBPY.extract_data import get_time_eaf
from src.page5.snl_stats_visualization_page5 import plot_track_previous_expression, plot_track_following_expression, \
    plot_track_previous_expression_byI, plot_track_following_expression_byI, plot_mimicry
from src.snl_stats_extraction_data import get_parameters_tag, get_parameters, expression_track, expression_track_byI, \
    give_mimicry_folder2, get_tier_dict_conv_folder, get_tier_from_tier, give_mimicry_folder4

dash.register_page(__name__, path='/mimicry/')


def update_entity_radio_entity_stats(person, expression):
    entities = get_entities(expression)

    if expression is not None:
        if len(entities) > 0:
            return radio_items([[entity, entity] for entity in entities]), f"Select an entity for person {person} ({expression})" , entities[0], None
        else:
            return [], f"Select an entity for person {person} ({expression})", None, None
    else:
        return [], None , None, "hidden"

layout = section_container("Mimicked Expression", "Check the capacity of someone to mimic someone else expression in an interaction.", children=[
    select(
        label="Select a database",
        id="database-select-mimicry",
        options=[],
    ),
    radio(
        id="pov-radio-mimicry",
        label="Select a point of view",
        value="A/B",
        options=[["A/B", "A mimicking B"], ["B/A", "B mimicking A"]],
    ),
    select(
        label="Select an expression (person A)",
        id="expression-A-select-mimicry",
        options=[],
    ),
    select(
        label="Select an expression (person B)",
        id="expression-B-select-mimicry",
        options=[],
    ),

    accordion(
        multiple=True,
        value=["all", "entity"],
        children=[
        accordion_item(
            label="All entities",
            description="",
            value="all",
            children=[
                dmc.NumberInput(
                    id="delta-input-mimicry-all",
                    label="Delta time in ms",
                    description="Time after which expression occuring still counts as mimicry.py",
                    value=0,
                    min=0,
                    radius="md",
                ),
                html.Div(className="flex flex-col gap-4", id="output-mimicry-all", children=[]),
                html.Span("Statistics divided by expressions", className="text-md font-medium"),
                html.Div(children=[
                    select(
                        label="Select an expression",
                        id="expression-select-mimicry-all-stats",
                        options=[],
                    ),
                    radio(
                        id="entity-A-radio-mimicry-all-stats",
                        label="",
                        options=[],
                    ),
                    radio(
                        id="entity-B-radio-mimicry-all-stats",
                        label="",
                        options=[],
                    ),
                    html.Div(className="flex flex-col gap-4", id="output-mimicry-all-stats", children=[]),
                ], className="flex flex-col gap-4 px-4"),
            ]
        ),
        accordion_item(
            label="By entity",
            description="",
            value="entity",
            children=[
                radio(
                    id="entity-A-radio-mimicry-entity",
                    label="Select an entity (for Laughs_0 of person A)",
                    options=[],
                ),
                radio(
                    id="entity-B-radio-mimicry-entity",
                    label="Select an entity (for Laughs_0 of person B)",
                    options=[],
                ),
                dmc.NumberInput(
                    id="delta-input-mimicry-entity",
                    label="Delta time in ms",
                    description="Time after which expression occuring still counts as mimicry.py",
                    value=0,
                    min=0,
                    radius="md",

                ),
                html.Div(className="flex flex-col gap-4", id="output-mimicry-entity", children=[]),
                html.Span("Statistics divided by expressions", className="text-md font-medium"),
                html.Div(children=[
                    select(
                        label="Select an expression",
                        id="expression-select-mimicry-entity-stats",
                        options=[],
                    ),
                    radio(
                        id="entity-A-radio-mimicry-entity-stats",
                        label="",
                        options=[],
                    ),
                    radio(
                        id="entity-B-radio-mimicry-entity-stats",
                        label="",
                        options=[],
                    ),
                    html.Div(className="flex flex-col gap-4", id="output-mimicry-entity-stats", children=[]),
                ], className="flex flex-col gap-4 px-4"),
            ],
        ),
    ]),
])


@callback(
    Output('database-select-mimicry', 'data'),
    Input('url', 'pathname'))
def update_database_select(pathname):
    return get_databases_select()


@callback(
    [Output('expression-A-select-mimicry', 'data'), Output('expression-B-select-mimicry', 'data')],
    Input('url', 'pathname'))
def update_expression_select(pathname):
    options = get_expressions_select()
    return options, options


@callback(
    [Output('expression-select-mimicry-entity-stats', 'data'), Output('expression-select-mimicry-all-stats', 'data')],
    [Input('expression-A-select-mimicry', 'value'), Input('expression-B-select-mimicry', 'value')])
def update_expression_divided_stats_select(expression_A, expression_B):
    if expression_A is None or expression_B is None:
        return [], []

    name_tiers = get_expressions()
    output = [{"label": tier, "value": tier} for tier in name_tiers if tier != expression_B and tier != expression_A]

    return output, output

@callback(
    [Output('delta-input-mimicry-entity', 'max'), Output('delta-input-mimicry-all', 'max')],
    Input('database-select-mimicry', 'value'))
def update_delta_max(database):
    if database is None:
        return 0, 0

    database_paths = get_database_paths(database)

    max_eaf_durations = get_time_eaf(database_paths, tiers=None)
    max = min(max_eaf_durations) * 1000
    return max, max


@callback(
    Output('output-mimicry-all', 'children'),
    [Input('database-select-mimicry', 'value'),
     Input('expression-A-select-mimicry', 'value'),
     Input('expression-B-select-mimicry', 'value'),
     Input('pov-radio-mimicry', 'value'),
     Input('delta-input-mimicry-all', 'value')])
def update_output_mimicry_all(database, expression_A, expression_B, pov, delta):

    if database is None or expression_A is None or expression_B is None or pov is None or delta is None or delta == "":
        return []

    database_paths = get_database_paths(database)


    try:
        figure_count, figure_proba, df = plot_mimicry(
            give_mimicry_folder2(
                database_paths,
                database.lower(),
                get_tier_dict_conv_folder,
                get_tier_dict_conv_folder,
                expression_A,
                expression_B,
                delta_t=delta,
                mimic_choice=pov)
        )

        return [
            dcc.Graph(figure=figure_count),
            dcc.Graph(figure=figure_proba),
        ]

    except Exception as e:
        return "No data available"


@callback(
    Output('output-mimicry-all-stats', 'children'),
    [Input('database-select-mimicry', 'value'),
     Input('expression-A-select-mimicry', 'value'),
     Input('expression-B-select-mimicry', 'value'),
     Input('entity-A-radio-mimicry-all-stats', 'value'),
     Input('entity-B-radio-mimicry-all-stats', 'value'),
     Input('pov-radio-mimicry', 'value'),
     Input('delta-input-mimicry-all', 'value'),
     Input('expression-select-mimicry-all-stats', 'value')])
def update_output_mimicry_all(database, expression_A, expression_B, entity_A, entity_B, pov, delta, tier_filter):
    if database is None or expression_A is None or expression_B is None or entity_A is None or entity_B is None or pov is None or delta is None or delta == "" or tier_filter is None:
        return []

    database_paths = get_database_paths(database)

    try:
        figure_count, figure_proba, df = plot_mimicry(
            give_mimicry_folder4(
                database_paths,
                database.lower(),
                get_tier_from_tier,
                get_tier_from_tier,
                expression_A,
                expression_B,
                tier_filter=tier_filter,
                entity1=entity_A,
                entity2=entity_B,
                delta_t=delta,
                mimic_choice=pov)
        )

        return [
            dcc.Graph(figure=figure_count),
            dcc.Graph(figure=figure_proba),
        ]

    except Exception as e:
        return "No data available"


@callback(
    Output('output-mimicry-entity', 'children'),
    [Input('database-select-mimicry', 'value'),
     Input('expression-A-select-mimicry', 'value'),
     Input('expression-B-select-mimicry', 'value'),
     Input('entity-A-radio-mimicry-entity', 'value'),
     Input('entity-B-radio-mimicry-entity', 'value'),
     Input('pov-radio-mimicry', 'value'),
     Input('delta-input-mimicry-entity', 'value')])
def update_output_mimicry_entity(database, expression_A, expression_B, entity_A, entity_B, pov, delta):
    if database is None or expression_A is None or expression_B is None or pov is None or delta is None or delta == "":
        return []

    database_paths = get_database_paths(database)
    try:
        figure_count, figure_proba, df = plot_mimicry(
            give_mimicry_folder2(
                database_paths,
                database.lower(),
                get_tier_dict_conv_folder,
                get_tier_dict_conv_folder,
                expression_A,
                expression_B,
                'Intensity',
                [entity_A, entity_B],
                delta_t=delta,
                mimic_choice=pov
            )
        )

        return [
            dcc.Graph(figure=figure_count),
            dcc.Graph(figure=figure_proba),
        ]

    except Exception as e:
        return "No data available"


@callback(
    Output('output-mimicry-entity-stats', 'children'),
    [Input('database-select-mimicry', 'value'),
     Input('expression-A-select-mimicry', 'value'),
     Input('expression-B-select-mimicry', 'value'),
     Input('entity-A-radio-mimicry-entity', 'value'),
     Input('entity-B-radio-mimicry-entity', 'value'),
     Input('pov-radio-mimicry', 'value'),
     Input('delta-input-mimicry-entity', 'value'),
     Input('expression-select-mimicry-entity-stats', 'value'),
     Input('entity-A-radio-mimicry-entity-stats', 'value'),
     Input('entity-B-radio-mimicry-entity-stats', 'value')])
def update_output_mimicry_entity_stats(database, expression_A, expression_B, entity_A, entity_B, pov, delta, tier_filter, entity_A_stats, entity_B_stats):
    if database is None or expression_A is None or expression_B is None or pov is None or delta is None or delta == "" or tier_filter is None or entity_A is None or entity_B is None or entity_A_stats is None or entity_B_stats is None:
        return []

    database_paths = get_database_paths(database)
    try:
        figure_count, figure_proba, df = plot_mimicry(
            give_mimicry_folder4(
                database_paths,
                database.lower(),
                get_tier_from_tier,
                get_tier_from_tier,
                expression_A,
                expression_B,
                tier_filter=tier_filter,
                entity1=entity_A_stats,
                entity2=entity_B_stats,
                filter='Intensity',
                label=[str.lower(entity_A), str.lower(entity_B)],
                delta_t=delta,
                mimic_choice=pov
            )
        )

        return [
            dcc.Graph(figure=figure_count),
            dcc.Graph(figure=figure_proba),
        ]

    except Exception as e:
        return "No data available"


@callback(
    [Output('entity-A-radio-mimicry-entity-stats', 'children'), Output('entity-A-radio-mimicry-entity-stats', 'label'), Output("entity-A-radio-mimicry-entity-stats", "value"), Output("entity-A-radio-mimicry-entity-stats", "className")],
    Input('expression-select-mimicry-entity-stats', 'value'))
def update_entity_A_radio_entity_stats(expression):
    return update_entity_radio_entity_stats('A', expression)


@callback(
    [Output('entity-B-radio-mimicry-entity-stats', 'children'), Output('entity-B-radio-mimicry-entity-stats', 'label'), Output("entity-B-radio-mimicry-entity-stats", "value"), Output("entity-B-radio-mimicry-entity-stats", "className")],
    Input('expression-select-mimicry-entity-stats', 'value'))
def update_entity_B_radio_entity_stats(expression):
    return update_entity_radio_entity_stats('B', expression)


@callback(
    [Output('entity-A-radio-mimicry-all-stats', 'children'), Output('entity-A-radio-mimicry-all-stats', 'label'), Output("entity-A-radio-mimicry-all-stats", "value"), Output("entity-A-radio-mimicry-all-stats", "className")],
    Input('expression-select-mimicry-all-stats', 'value'))
def update_entity_A_radio_all_stats(expression):
    return update_entity_radio_entity_stats('A', expression)


@callback(
    [Output('entity-B-radio-mimicry-all-stats', 'children'), Output('entity-B-radio-mimicry-all-stats', 'label'), Output("entity-B-radio-mimicry-all-stats", "value"), Output("entity-B-radio-mimicry-all-stats", "className")],
    Input('expression-select-mimicry-all-stats', 'value'))
def update_entity_B_radio_all_stats(expression):
    return update_entity_radio_entity_stats('B', expression)


@callback(
    [Output('entity-A-radio-mimicry-entity', 'children'), Output('entity-A-radio-mimicry-entity', 'label'), Output("entity-A-radio-mimicry-entity", "value"), Output("entity-A-radio-mimicry-entity", "className")],
    Input('expression-A-select-mimicry', 'value'))
def update_entity_A_radio(expression):
    return update_entity_radio_entity_stats('A', expression)


@callback(
    [Output('entity-B-radio-mimicry-entity', 'children'), Output('entity-B-radio-mimicry-entity', 'label'), Output("entity-B-radio-mimicry-entity", "value"), Output("entity-B-radio-mimicry-entity", "className")],
    Input('expression-B-select-mimicry', 'value'))
def update_entity_B_radio(expression):
    return update_entity_radio_entity_stats('B', expression)

