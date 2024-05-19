from Dash.components.containers.accordion import accordion, accordion_item
from Dash.components.containers.section import section_container
from Dash.components.interaction.radio import radio
from Dash.components.interaction.select import select
from dash import html



def create_table(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    return [html.Thead(header), html.Tbody(rows)]


def display_durations_intra(database):
    return section_container("Intra Non Verbal Expressions Analysis", "It's an analysis based on each individual. We look here at the sequence of expressions of each individual in each eaf file of the datasets.", children=[
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
                        allowDeselect=True,
                        id="database-select-durations-intra-dataset",
                        options=[]
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
                    html.Div(className="flex flex-col gap-4", id="output-durations-intra", children=[]),
                ]
            ),
            accordion_item(
                label="Divided by expressions for a specific dataset",
                value="expression",
                children=[
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-per-minute-entity",
                        options=[]
                    ),
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-per-minute-entity",
                        options=[]
                    ),
                    select(
                        label="Select a database",
                        allowDeselect=True,
                        id="database-select-per-minute",
                        options=[]
                    ),
                    radio(
                        id="entity-radio-per-minute-entity",
                        label="Select an figure",
                        options=[[None, "Scatter"], [2, "Line"]],
                    ),
                    html.Div(className="flex flex-col gap-4", id="output-per-minute-entity", children=[]),

                ],
            ),
        ]),
    ])
