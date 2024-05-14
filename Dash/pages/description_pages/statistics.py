from dash import html, callback, Output, Input
import pandas as pd
import dash_mantine_components as dmc
import numpy as np

from IBPY.extract_data import get_tier_intensities, get_max_min_time_tier, get_time_eaf, get_tier_count
from src.page3.snl_stats_visualization_database import display_general_informations_files, display_specific_informations
from src.snl_stats_extraction_data import get_parameters, get_parameters_tag
from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container, sub_section_container
from Dash.components.interaction.select import select
from Dash.components.interaction.radio import radio
from Dash.components.containers.accordion import accordion, accordion_item
import os


def create_table(df):
    columns, values = df.columns, df.values
    header = [html.Tr([html.Th(col) for col in columns])]
    rows = [html.Tr([html.Td(cell) for cell in row]) for row in values]
    return [html.Thead(header), html.Tbody(rows)]


def display_statistics_informations(database):
    return section_container("Statistics on non verbal expressions", "We look at some basic statistics about the database.", children=[
        accordion(
            multiple=True,
            value=["normal", "divided"],
            children=[
            accordion_item(
                label="By dataset",
                value="normal",
                children=[
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-statistics-normal",
                        options=[]
                    ),
                    select(
                        label="Select a statistic",
                        allowDeselect=True,
                        id="statistics-select-statistics-normal",
                        options=[]
                    ),
                    radio(
                        id="type-radio-statistics-normal",
                        label="Select a type",
                        options=[["absolute", "Absolute"], ["relative", "Relative"]],
                    )
                ]
            ),
            accordion_item(
                label="Divided by expressions",
                value="divided",
                children=[
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-statistics-divided",
                        options=[]
                    ),
                    select(
                        label="Select a statistic",
                        allowDeselect=True,
                        id="statistics-select-statistics-divided",
                        options=[]
                    ),
                    radio(
                        id="type-radio-statistics-divided",
                        label="Select a type",
                        options=[["absolute", "Absolute"], ["relative", "Relative"]],
                    )
                ],
            ),
        ]),
        html.Div(className="flex flex-col gap-4", id="per-minute-output", children=[]),
    ])


@callback(
    [Output('expression-select-statistics-divided', 'data'), Output('expression-select-statistics-normal', 'data')],
    Input('url', 'pathname'))
def update_expression_select(pathname):
    real_tier_lists, real_tiers = get_parameters_tag()
    lst_tiers_choice = []

    for tier in real_tier_lists.keys():
        if real_tier_lists[tier]['Intensities'] != None or real_tier_lists[tier]['Replace_Value'] != "":
            lst_tiers_choice.append(tier)

    name_tiers = lst_tiers_choice + ["all"]

    tiers_data = [{"label": tier, "value": tier} for tier in name_tiers]

    return tiers_data, tiers_data



