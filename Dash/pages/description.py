import dash
from dash import html,dcc, callback, Output, Input
import dash_mantine_components as dmc

from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container
from Dash.components.interaction.select import select
from Dash.pages.description_pages.information import display_general_informations

from src.json_creation import create_json_from_directory


dash.register_page(
    __name__,
    path="/description/",
)

options = [
    {"label": "Database informations", "value": "/description/"},
    {"label": "Expression per minute", "value": "/description/per_minute"},
    {"label": "Statistics", "value": "/description/stats"},
]


layout = page_container("Description", [
    html.Div(className="nav-section-container", children=select(
        label="Select a page",
        value="/description/",
        id="page-select",
        options=options),
    ),
    section_container("","" ,[
        html.Div(id='page-content'),
    ]),


])


@callback(
    Output('url', 'pathname'),
    Input('page-select', 'value')
)
def update_url(value):
    return value



@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/description/':
        # return "Contenu de la page Database informations"
        return display_general_informations("database")
    elif pathname == '/description/per_minute':
        return "Contenu de la page Expression per minute"
    elif pathname == '/description/stats':
        return "Contenu de la page Statistics"
    else:
        return "Page non trouvée"