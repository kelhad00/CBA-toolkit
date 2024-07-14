import dash
import numpy as np
import pandas as pd
import os

from app.components.callbacks.dataset import get_databases_select, get_database_paths
from app.components.callbacks.entity import get_entities
from app.components.callbacks.expression import get_expressions
from app.components.containers.section import section_container
from app.components.interaction.button import download_button
from app.components.interaction.select import select
from dash import html, callback, Output, Input
import dash_mantine_components as dmc

from app.components.interaction.table import create_table
from IBPY.extract_data import get_tier_intensities, get_max_min_time_tier
from src.description.snl_stats_visualization_database import display_general_informations_files
from src.snl_stats_extraction_data import get_parameters_tag, get_parameters

dash.register_page(
    __name__,
    path="/description/",
)


layout = section_container("Database informations", "", children=[
        select(
            label="Select a database",
            allowDeselect=True,
            id="database-select",
            options=[]
        ),
        select(
            label="Select an expression",
            value="GENERAL",
            allowDeselect=True,
            id="expression-select",
            options=[]
        ),
        html.Div(className="flex flex-col gap-4 overflow-x-scroll", id="information-output", children=[]),
    ])




@callback(
    Output('database-select', 'data'),
    Input('url', 'pathname'))
def update_database_select(pathname):
    return get_databases_select()



@callback(
    Output('expression-select', 'data'),
    Input('url', 'pathname'))
def update_expression_select(pathname):
    name_tiers = get_expressions() + ["GENERAL"]

    return [
        {"label": tier, "value": tier} for tier in name_tiers
    ]


@callback(
    Output('information-output', 'children'),
    [Input('database-select', 'value'),
     Input('expression-select', 'value')])
def update_information_output(database, expression):
    real_tier_lists, real_tiers = get_parameters_tag()

    if database is None or expression is None:
        return []

    database_paths = get_database_paths(database)

    if expression == "GENERAL":
        data = display_general_informations_files(database_paths)
        columns_names = ["Filename", "Duration"] + list(real_tier_lists.keys())
        df = pd.DataFrame(data, columns=columns_names)
        if df is not None:
            csv = df.to_csv(index=False)
            data = df.to_dict('records')
            return [
                dmc.Table(
                    highlightOnHover=True,
                    children=create_table(df)
                ),
                download_button(csv, "database_general.csv")
            ]
        else:
            return html.Div("No data available")

    else:
        lst = []
        lst_tier_count = get_tier_intensities(
            database_paths,
            expression,
            get_entities(expression),
            real_tier_lists[expression].get('Kind')
        )
        lst_min_time, lst_max_time = get_max_min_time_tier(database_paths, expression)
        temp = []
        for i in range(len(database_paths)):
            for intensity in get_entities(expression):
                temp.append(lst_tier_count[i][intensity])
            file_info = os.path.split(database_paths[i])[-1], lst_min_time[i], lst_max_time[i], *temp[:len(temp)]
            lst.append(file_info)
            temp.clear()

        columns_names = ["Filename", "Min duration", "Max duration"] + get_entities(expression)
        df = pd.DataFrame(lst, columns=columns_names)
        df = df.fillna(0)
        df = df.replace([np.inf, -np.inf], 0)
        return dmc.Table(
                    highlightOnHover=True,
                    children=create_table(df)
                )

