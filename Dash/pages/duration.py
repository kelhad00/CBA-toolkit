import dash
from dash import html, callback, Output, Input

from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container
from Dash.components.interaction.select import select
from Dash.pages.duration_pages.inter import display_durations_inter
from Dash.pages.duration_pages.intra import display_durations_intra

dash.register_page(__name__, path='/durations/intra', path_template="/durations/<page>",
)


options = [
    {"label": "Intra Non Verbal Expressions Analysis", "value": "/durations/intra"},
    {"label": "Inter Non Verbal Expressions Analysis", "value": "/durations/inter"},
]

layout = page_container("Durations", [
    html.Div(className="nav-section-container", children=select(
        label="Select a page",
        value="/durations/intra",
        id="page-select",
        options=options),
    ),
    section_container("", "", [
        html.Div(id='durations-page-content'),
    ]),
])



@callback(
    Output('durations-page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/durations/intra':
        return display_durations_intra("")
    elif pathname == '/durations/inter':
        return display_durations_inter("")
    else:
        return "Page non trouvée"

