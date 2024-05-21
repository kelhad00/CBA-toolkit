from Dash.components.containers.accordion import accordion, accordion_item
from Dash.components.containers.section import section_container
from Dash.components.interaction.radio import radio
from Dash.components.interaction.select import select
from dash import html
import dash


dash.register_page(
    __name__,
    path='/durations/inter',
)

layout = section_container("Inter Non Verbal Expressions Analysis", "It's an analysis based on each interaction between two persons. All figures are based on the duration of the expressions of each interaction (so two files) in the datasets.", children=[
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
