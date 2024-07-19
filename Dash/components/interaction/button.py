import dash_mantine_components as dmc
from dash import html


def download_button(csv, name="data.csv"):
    return dmc.Button(className="w-fit", radius="md", children=[
        html.A(
            'Download CSV',
            download=name,
            href="data:text/csv;charset=utf-8," + csv,
            target="_blank",
        )
    ])