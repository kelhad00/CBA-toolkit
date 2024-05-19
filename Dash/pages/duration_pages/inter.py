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


def display_durations_inter(database):
    return section_container("Inter Non Verbal Expressions Analysis", "It's an analysis based on each interaction between two persons. All figures are based on the duration of the expressions of each interaction (so two files) in the datasets.", children=[
        accordion(
            multiple=True,
            value=["all", "entity"],
            children=[
            accordion_item(
                label="By dataset",
                description="Display the number of expressions per minute for all entities in the database.",
                value="all",
                children=[
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-per-minute-all",
                        options=[]
                    ),
                    select(
                        label="Select a database",
                        allowDeselect=True,
                        id="database-select-per-minute",
                        options=[]
                    ),
                    radio(
                        id="pov-radio-per-minute-all",
                        label="Select a figure",
                        options=[[None, "Scatter"], [2, "Line"]],
                    ),
                    select(
                        label="Select a database",
                        allowDeselect=True,
                        id="database-select-per-minute",
                        options=[]
                    ),
                    radio(
                        id="pov-radio-per-minute-all",
                        label="Select a figure",
                        options=[[None, "Scatter"], [2, "Line"]],
                    ),
                    html.Div(className="flex flex-col gap-4", id="output-per-minute-all", children=[]),
                ]
            ),
            accordion_item(
                label="Divided by expressions for a specific dataset",
                description="We are looking at the stats of a specific expression to analyse compare to another one during an interaction.",
                value="entity",
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
