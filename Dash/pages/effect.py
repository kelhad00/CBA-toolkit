import dash
from dash import html

from Dash.components.containers.page import page_container

dash.register_page(__name__, path='/effects/')

# layout = page_container("Effects", [])

layout = html.Div("Effects")