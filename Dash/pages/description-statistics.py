import dash
from dash import html, Output, Input, callback, dcc

import dash_mantine_components as dmc

from Dash.components.containers.accordion import accordion, accordion_item
from Dash.components.containers.section import section_container
from Dash.components.interaction.radio import radio
from Dash.components.interaction.select import select
from src.page3.snl_stats_visualization_page3 import plot_absolute_duration, plot_relative_duration, \
    plot_absolute_duration_from_tier, plot_relative_duration_from_tier
from src.snl_stats_extraction_data import get_parameters_tag, get_parameters

statistics_list = ["All", "Standard deviation", "Mean", "Median", "Max", "Min"]
statistics_options = [{"label": stat, "value": stat} for stat in statistics_list]


dash.register_page(
    __name__,
    path="/description/stats",
)


layout = section_container("Statistics on non verbal expressions", "We look at some basic statistics about the database.", children=[
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
                        value="All",
                        options=statistics_options
                    ),
                    radio(
                        id="type-radio-statistics-normal",
                        label="Select a type",
                        value="absolute",
                        options=[["absolute", "Absolute"], ["relative", "Relative"]],
                    ),
                    html.Div(id="output-statistics-normal")

                ]
            ),
            accordion_item(
                label="Divided by expressions",
                value="divided",
                children=[
                    select(
                        label="Select an expression (divided by)",
                        allowDeselect=True,
                        id="expression-select-statistics-divided",
                        options=[]
                    ),
                    select(
                        label="Select an expression (analyzed)",
                        allowDeselect=True,
                        id="analyzed-expression-select-statistics-divided",
                        options=[]
                    ),
                    select(
                        label="Select a statistic",
                        allowDeselect=True,
                        value="All",
                        id="statistics-select-statistics-divided",
                        options=statistics_options
                    ),
                    radio(
                        id="type-radio-statistics-divided",
                        label="Select a type",
                        value="absolute",
                        options=[["absolute", "Absolute"], ["relative", "Relative"]],
                    ),
                    html.Div(id="output-statistics-divided")

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

    tiers_data_all = [{"label": tier, "value": tier} for tier in name_tiers]
    tiers_data = [{"label": tier, "value": tier} for tier in lst_tiers_choice]

    return tiers_data, tiers_data_all


@callback(
    [Output('analyzed-expression-select-statistics-divided', 'data'),
     Output('analyzed-expression-select-statistics-divided', 'value')],
    Input('expression-select-statistics-divided', 'value')
)
def update_analyzed_expression_select(expression):
    if (expression is None):
        return [], None

    real_tier_lists, real_tiers = get_parameters_tag()
    lst_tiers_choice = []

    for tier in real_tier_lists.keys():
        if real_tier_lists[tier]['Intensities'] != None or real_tier_lists[tier]['Replace_Value'] != "":
            lst_tiers_choice.append(tier)

    name_tiers = lst_tiers_choice + ["all"]

    return [{"label": tier, "value": tier} for tier in name_tiers if tier != expression], None


@callback(
    Output('output-statistics-normal', 'children'),
    [Input('expression-select-statistics-normal', 'value'),
     Input('statistics-select-statistics-normal', 'value'),
     Input('type-radio-statistics-normal', 'value')]
)
def update_statistics_normal(expression, statistic, type):
    real_tier_lists, real_tiers = get_parameters_tag()
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    name_databases = [key.replace('_paths', '').upper() for key in databases.keys()]

    if expression is None or statistic is None or type is None:
        return []

    try:
        if expression != 'all':
            if real_tier_lists[expression]:
                if type == 'absolute':
                    fig1_0, df1_0 = plot_absolute_duration(expression, statistic, name_databases)
                    print(fig1_0)
                    return dcc.Graph(figure=fig1_0)
                else:
                    fig2_0, df2_0 = plot_relative_duration(expression, statistic, name_databases)
                    return dcc.Graph(figure=fig2_0)


        else:
            figures1 = []
            if type == 'absolute':
                fig1_1 = plot_absolute_duration(expression, statistic, name_databases)
                figures1.extend(fig1_1)
            else:
                fig2_1 = plot_relative_duration(expression, statistic, name_databases)
                figures1.extend(fig2_1)

            return [dcc.Graph(figure=fig) for fig in figures1 if fig is not None]

        return f"No Data available for {expression}"

    except Exception as e:
        print(e)
        return f"No Data available for {expression}"


@callback(
    Output('output-statistics-divided', 'children'),
    [
        Input('expression-select-statistics-divided', 'value'),
        Input('analyzed-expression-select-statistics-divided', 'value'),
        Input('statistics-select-statistics-divided', 'value'),
        Input('type-radio-statistics-divided', 'value')
    ]
)
def update_statistics_divided(expression_divided, expression_analyzed, statistic, type):
    real_tier_lists, real_tiers = get_parameters_tag()
    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
    name_databases = [key.replace('_paths', '').upper() for key in databases.keys()]

    if expression_divided is None or expression_analyzed is None or statistic is None or type is None:
        return []

    if real_tier_lists[expression_divided]['Replace_Value'] != "":
        expression_values = [real_tier_lists[expression_divided]['Replace_Value'],
                             str("No_" + real_tier_lists[expression_divided]['Replace_Value'])]
    else:
        expression_values = real_tier_lists[expression_divided]['Intensities']

    try:
        if expression_analyzed != 'all':
            if real_tier_lists[expression_analyzed]:
                if type == "absolute":
                    figures = []
                    for entity in expression_values:
                        fig1_temp, df1_temp = plot_absolute_duration_from_tier(expression_divided, entity,
                                                                               expression_analyzed, statistic,
                                                                               name_databases)
                        figures.append(fig1_temp)

                    if all(fig is None for fig in figures):
                        return f"No data available for {expression_divided} and {expression_analyzed}"
                    else:
                        return [dcc.Graph(figure=fig) for fig in figures if fig is not None]

                else:
                    figures = []
                    for entity in expression_values:
                        fig1_temp, df1_temp = plot_relative_duration_from_tier(expression_divided, entity,
                                                                               expression_analyzed, statistic,
                                                                               name_databases)
                        figures.extend(fig1_temp)

                    if all(fig is None for fig in figures):
                        return f"No data available for {expression_divided} and {expression_analyzed}"
                    else:
                        return [dcc.Graph(figure=fig) for fig in figures if fig is not None]

            else:
                return f"No data available for {expression_analyzed} with {expression_divided}"

        else:
            figures = []
            print("here")
            if type == "absolute":
                for entity in expression_values:
                    fig1_temp = plot_absolute_duration_from_tier(expression_divided, entity, expression_analyzed,
                                                                 statistic, name_databases)
                    figures.extend(fig1_temp)
                    print(entity)
            else:
                for entity in expression_values:
                    fig1_temp = plot_relative_duration_from_tier(expression_divided, entity, expression_analyzed,
                                                                 statistic, name_databases)
                    figures.extend(fig1_temp)
            print("figure ", len(figures))

            if all(fig is None for fig in figures):
                return f"No data available for {expression_divided} and {expression_analyzed}"
            else:
                return [dcc.Graph(figure=fig) for fig in figures if fig is not None]



    except Exception as e:
        print(e)
        return f"No Data available for {expression_divided} and {expression_analyzed}"

    return "No Data available"
