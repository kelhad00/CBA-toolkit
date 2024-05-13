# from dash import html, dcc, callback, Output, Input
# from src.snl_stats_extraction_data import get_parameters, get_parameters_tag
# from Dash.components.containers.page import page_container
# from Dash.components.containers.section import section_container
# from Dash.components.interaction.select import select
#
#
# def display_general_informations(database):
#     return section_container("Database informations", "", children=[
#         html.Div(id="database_select-container", children=
#             select(label="Select a database", value="database", id="database-select", options=[]),
#         ),
#     ])
#     @callback(
#         Output('database-select-container', 'children'),
#         Input('url', 'pathname'),suppress_callback_exceptions=True)
#     def update_database_select(pathname):
#         DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
#         name_databases = [key.replace('_paths', '').upper() for key in databases.keys()]
#         return select(label="Select a database", value="database", id="database-select", options=[
#             {"label": database, "value": database} for database in name_databases
#         ]),
#
#
#
