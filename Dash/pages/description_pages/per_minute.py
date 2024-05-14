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


def display_per_minute_informations(database):
    return section_container("Expression Per Minute", "We count the number of expressions/tiers we have in one minute in each dataset.", children=[
        select(
            label="Select a database",
            allowDeselect=True,
            id="database-select-per-minute",
            options=[]
        ),
        accordion(
            multiple=True,
            value=["all", "entity"],
            children=[
            accordion_item(
                label="All entities",
                description="Display the number of expressions per minute for all entities in the database.",
                value="all",
                children=[
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-per-minute-all",
                        options=[]
                    ),
                    radio(
                        id="pov-radio-per-minute-all",
                        label="Select a point of view",
                        options=[["intra", "Intra"], ["inter", "Inter"]],
                    )
                ]
            ),
            accordion_item(
                label="By entity",
                description="Display the number of expressions per minute by entity in the database.",
                value="entity",
                children=[
                    select(
                        label="Select an expression",
                        allowDeselect=True,
                        id="expression-select-per-minute-entity",
                        options=[]
                    ),
                    radio(
                        id="entity-radio-per-minute-all",
                        label="Select an entity",
                        options=[],
                    )
                ],
            ),
        ]),
        html.Div(className="flex flex-col gap-4", id="per-minute-output", children=[]),
    ])


@callback(
    Output('database-select-per-minute', 'data'),
    Input('url', 'pathname'))
def update_database_select(pathname):
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    name_databases = [key.replace('_paths', '').upper() for key in databases.keys()]
    return [
        {"label": database, "value": database} for database in name_databases
    ]


@callback(
    [Output('expression-select-per-minute-all', 'data'), Output('expression-select-per-minute-entity', 'data')],
    Input('url', 'pathname'))
def update_expression_select(pathname):
    real_tier_lists, real_tiers = get_parameters_tag()
    lst_tiers_choice = []

    for tier in real_tier_lists.keys():
        if real_tier_lists[tier]['Intensities'] != None or real_tier_lists[tier]['Replace_Value'] != "":
            lst_tiers_choice.append(tier)

    name_tiers = lst_tiers_choice

    tiers_data = [{"label": tier, "value": tier} for tier in name_tiers]

    return tiers_data, tiers_data



