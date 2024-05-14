from dash import html, dcc, callback, Output, Input
import pandas as pd
import dash_mantine_components as dmc
import numpy as np

from IBPY.extract_data import get_tier_intensities, get_max_min_time_tier, get_time_eaf, get_tier_count
from src.page3.snl_stats_visualization_database import display_general_informations_files, display_specific_informations
from src.snl_stats_extraction_data import get_parameters, get_parameters_tag
from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container
from Dash.components.interaction.select import select
import os

def create_table(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    table = [html.Thead(header), html.Tbody(rows)]
    return table


def display_general_informations(database):
    return section_container("Database informations", "", children=[
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
        html.Div(className="flex flex-col gap-4", id="information-output", children=[]),
    ])

@callback(
    Output('database-select', 'data'),
    Input('url', 'pathname'))
def update_database_select(pathname):
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    name_databases = [key.replace('_paths', '').upper() for key in databases.keys()]
    return [
        {"label": database, "value": database} for database in name_databases
    ]



@callback(
    Output('expression-select', 'data'),
    Input('url', 'pathname'))
def update_expression_select(pathname):
    real_tier_lists, real_tiers = get_parameters_tag()
    lst_tiers_choice = []

    for tier in real_tier_lists.keys():
        if real_tier_lists[tier]['Intensities'] != None or real_tier_lists[tier]['Replace_Value'] != "":
            lst_tiers_choice.append(tier)

    name_tiers = lst_tiers_choice + ["GENERAL"]

    return [
        {"label": tier, "value": tier} for tier in name_tiers
    ]


@callback(
    Output('information-output', 'children'),
    [Input('database-select', 'value'),
     Input('expression-select', 'value')])
def update_information_output(database, expression):
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    real_tier_lists, real_tiers = get_parameters_tag()

    if database is None or expression is None:
        return []

    print()
    database = databases_paths[database.lower() + "_paths"]

    if expression == "GENERAL":
        data = display_general_informations_files(database)
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
                dmc.Button(className="w-fit", radius="md", children=[
                    html.A(
                        'Download CSV',
                        id='download-link',
                        download="database_general.csv",
                        href="data:text/csv;charset=utf-8," + csv,
                        target="_blank",
                    )
                ])
            ]
        else:
            return html.Div("No data available")

    else:
        lst = []
        lst_tier_count = get_tier_intensities(database, expression,
                                              real_tier_lists[expression]['Intensities'],
                                              real_tier_lists[expression].get('Kind'))
        lst_min_time, lst_max_time = get_max_min_time_tier(database, expression)
        temp = []
        for i in range(len(database)):
            for intensity in real_tier_lists[expression]['Intensities']:
                temp.append(lst_tier_count[i][intensity])
            file_info = os.path.split(database[i])[-1], lst_min_time[i], lst_max_time[i], *temp[:len(temp)]
            lst.append(file_info)
            temp.clear()

        columns_names = ["Filename", "Min duration", "Max duration"] + real_tier_lists[expression]['Intensities']
        df = pd.DataFrame(lst, columns=columns_names)
        df = df.fillna(0)
        df = df.replace([np.inf, -np.inf], 0)
        return dmc.Table(
                    highlightOnHover=True,
                    children=create_table(df)
                )




