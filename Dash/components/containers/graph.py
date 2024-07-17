from dash import html, dcc

from Dash.components.interaction.button import download_button


def graph_container(figure, csv, name=None):
    return html.Div(className="flex flex-col gap-4", children=[
        dcc.Graph(figure=figure),
        download_button(csv, name) if csv != "\n" else None
    ])
