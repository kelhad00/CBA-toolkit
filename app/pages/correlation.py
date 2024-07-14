import dash
from dash import html, Output, callback, Input, dcc

from app.components.callbacks.dataset import get_database_paths, get_databases_select
from app.components.callbacks.entity import get_entities
from app.components.callbacks.expression import get_expressions_select
from app.components.containers.accordion import accordion, accordion_item
from app.components.containers.graph import graph_container
from app.components.containers.section import section_container
from app.components.interaction.radio import radio, radio_items
from app.components.interaction.select import select
from app.components.interaction.slider import slider

from src.effect.snl_stats_visualization_page5 import plot_correlation
from src.snl_stats_extraction_data import get_correlation_folder, get_correlation_byI, get_correlation_by_entity

dash.register_page(__name__, path='/correlation/')


def update_entities_radio(expression, entity):
    """ Update the radio items for the entities.
    Params:
        expression: The expression selected.
        entity: The entity selected.
    Return:
        list : radio option items.
    """
    if not expression:
        return []

    entities = get_entities(expression)
    if entity != "all":
        entities.append("all")

    return radio_items([[entity, entity] for entity in entities])


layout = section_container("Correlation Analysis", "Check if an expression has an effect on another one.", children=[
    select(
        label="Select a database",
        id="database-select-correlation",
        options=[],
    ),
    select(
        label="Select an expression (person A)",
        id="expression-A-select-correlation",
        options=[],
    ),
    select(
        label="Select an expression (person B)",
        id="expression-B-select-correlation",
        options=[],
    ),
    accordion(
        multiple=True,
        value=["entity", "all"],
        children=[
        accordion_item(
            label="By dataset",
            description="Analysis of the correlation between two expressions.",
            value="all",
            children=[
                slider(
                    id="width-slider-correlation",
                    minimum=1,
                    maximum=344,
                    label="Select the width (period/window in ms)"
                ),
                slider(
                    id="shift-slider-correlation",
                    minimum=1,
                    maximum=344,
                    label="Select the shift (shift in ms):"
                ),
                html.Div(className="flex flex-col gap-4", id="output-correlation-dataset", children=[]),
            ]
        ),
        accordion_item(
            label="By dataset and expression",
            description="Analysis of the correlation between two expressions or/and two entities during an interaction.",
            value="entity",
            children=[
                radio(
                    id="entity-A-radio-correlation-entity",
                    label="Select an entity (person A)",
                    options=[],
                ),
                radio(
                    id="entity-B-radio-correlation-entity",
                    label="Select an entity (person B)",
                    options=[],
                ),
                slider(
                    id="width-slider-correlation-entity",
                    minimum=1,
                    maximum=344,
                    label="Select the width (period/window in ms)"
                ),
                slider(
                    id="shift-slider-correlation-entity",
                    minimum=1,
                    maximum=344,
                    label="Select the shift (shift in ms):"
                ),
                html.Div(className="flex flex-col gap-4", id="output-correlation-entity", children=[]),
            ],
        ),
    ]),
])


@callback(
    Output("database-select-correlation", "data"),
    Input("url", "pathname")
)
def update_database_select(pathname):
    return get_databases_select()


@callback(
    [Output("expression-A-select-correlation", "data"), Output("expression-B-select-correlation", "data")],
    Input("url", "pathname")
)
def update_expression_select(pathname):
    options = get_expressions_select()
    return options, options


@callback(
    Output("output-correlation-dataset", "children"),
    Input("database-select-correlation", "value"),
    Input("expression-A-select-correlation", "value"),
    Input("expression-B-select-correlation", "value"),
    Input("width-slider-correlation", "value"),
    Input("shift-slider-correlation", "value"),
)
def update_output_mimicry_all(database, expression_A, expression_B, width, shift):
    if not database or not expression_A or not expression_B:
        return []

    database_paths = get_database_paths(database)

    figure, df = plot_correlation(
        get_correlation_folder(
            expression_A,
            database_paths,
            width,
            shift,
            expression_B
        ),
        database_paths
    )

    return graph_container(figure, df.to_csv(index=False), f"{expression_A}_{expression_B}_correlation")


@callback(
    [Output("entity-A-radio-correlation-entity", "children"), Output("entity-A-radio-correlation-entity", "label"),  Output("entity-A-radio-correlation-entity", "className")],
    [Input("entity-B-radio-correlation-entity", "value"), Input("expression-A-select-correlation", "value")],
)
def update_entity_A_radio(entity_B, expression_A):
    return update_entities_radio(expression_A, entity_B), f"Select an entity for person A ({expression_A})", "hidden" if expression_A is None else None


@callback(
    [Output("entity-B-radio-correlation-entity", "children"), Output("entity-B-radio-correlation-entity", "label"),  Output("entity-B-radio-correlation-entity", "className")],
    [Input("entity-A-radio-correlation-entity", "value"), Input("expression-B-select-correlation", "value")],
)
def update_entity_B_radio(entity_A, expression_B):
    return update_entities_radio(expression_B, entity_A),  f"Select an entity for person B ({expression_B})", "hidden" if expression_B is None else None


@callback(
    Output("output-correlation-entity", "children"),
    Input("database-select-correlation", "value"),
    Input("expression-A-select-correlation", "value"),
    Input("expression-B-select-correlation", "value"),
    Input("entity-A-radio-correlation-entity", "value"),
    Input("entity-B-radio-correlation-entity", "value"),
    Input("width-slider-correlation-entity", "value"),
    Input("shift-slider-correlation-entity", "value"),
)
def update_output_correlation_entity(database, expression_A, expression_B, entity_A, entity_B, width, shift):
    if not database or not expression_A or not expression_B or not entity_A or not entity_B:
        return []

    database_paths = get_database_paths(database)

    if entity_A == "all":
        figure, df = plot_correlation(
            get_correlation_by_entity(
                expression_B,
                entity_B,
                database_paths,
                width,
                shift,
                expression_A
            ),
            database_paths
        )
    elif entity_B == "all":
        figure, df = plot_correlation(
            get_correlation_by_entity(
                expression_A,
                entity_A,
                database_paths,
                width,
                shift,
                expression_B
            ),
            database_paths
        )
    else:
        figure, df = plot_correlation(
            get_correlation_byI(
                expression_A,
                entity_A,
                database_paths,
                width,
                shift,
                expression_B,
                entity_B
            ),
            database_paths
        )

    return graph_container(figure, df.to_csv(index=False), f"{expression_A}_{entity_A}_{expression_B}_{entity_B}_correlation")
