from datetime import datetime

import dash
from dash import html, dcc, callback, Input, Output, no_update
from dash.exceptions import PreventUpdate

from urllib.parse import parse_qs, unquote
import json
import os

from src.snl_stats_extraction_data import get_parameters, get_parameters_tag

from Dash.components.interaction.table import table_line, table_cell, table_container
from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container

dash.register_page(__name__, name='Tiers')

DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers = get_parameters()
tiers = tier_lists
real_tier_lists, real_tiers = get_parameters_tag()

print(real_tiers, real_tier_lists)


def display_table_line(tier, replace_value, real_tier_lists):
    print(tier in real_tier_lists.keys())
    return table_line([
        dcc.Checklist(options=[{
            "label": "Selected",
            "value": tier,
        }], value=[tier] if tier in real_tier_lists.keys() else [], id=f'{tier}-checkbox',
            labelStyle={"display": "flex"}, className="flex-1", labelClassName="flex gap-2 items-center"),
        table_cell("tier", tier),
        table_cell("replace_value", dcc.Input(id=f'{tier}-input', type="number",
                                              className="border border-2 border-gray-300 text-black rounded-md")),
    ])


layout = page_container("Tiers", [
    html.Div(id="output", className="hidden"),

    section_container("Max Intensity",
                      "Select a maximum of intensity for a tier to be considered without Replace_Value", [
                          dcc.Input(id="max_intensity", type="number", value=25,
                                    className="border border-2 border-gray-300 rounded-md p-2"),
                      ]),
    section_container("Selection", "Select the tiers to be considered", [
        display_table_line(tier, 0, real_tier_lists) for tier in tiers
    ], id="tiers_table"),
])


@callback(Output('tiers_table', 'children'), [Input('url', 'pathname')])
def update_tiers_table(pathname):
    real_tier_lists, real_tiers = get_parameters_tag()
    return [display_table_line(tier, 0, real_tier_lists) for tier in tiers]


@callback(
    Output('output', 'children'),
    [Input('max_intensity', 'value')] + [Input(f'{tier}-checkbox', 'value') for tier in tiers] + [
        Input(f'{tier}-input', 'value') for tier in tiers])
def update_output(*args):
    if not dash.callback_context.triggered:
        raise PreventUpdate

    max_intensity = args[0]
    selected_values = args[1:len(tiers) + 1]
    replace_values = args[len(tiers) + 1:]

    selected_values = [tier[0] for tier in selected_values if tier]
    checkbox_state = {f"{tier}_tag": tier in selected_values for tier in tiers}
    checkbox_state.update(
        {f"{tier}_replace": "" if replace is None else str(replace) for tier, replace in zip(tiers, replace_values)})
    checkbox_state['max_intensity'] = max_intensity

    lst_choice = []
    replace_choice = []
    Max_Intensity = checkbox_state['max_intensity']

    for label in checkbox_state.keys():
        option1_checked = checkbox_state[label]
        if option1_checked == True:
            lst_choice.append(label.replace('_tag', ''))

        if option1_checked == False:
            if label in lst_choice:
                lst_choice.remove(label.replace('_tag', ''))

        if option1_checked != False and option1_checked != True:

            if option1_checked:

                replace_choice.append(label.replace('_replace', ''))

            else:

                if label.replace('_replace', '') in replace_choice:
                    replace_choice.remove(label.replace('_tag', ''))

    with open('data.json') as json_file:
        data = json.load(json_file)
    dct = {}
    dct['TIER_LISTS'] = {}

    for key in data['TIER_LISTS'].keys():
        if key in lst_choice:
            try:
                #print path to json file
                print(os.path.abspath('base_data.json'))
                with open('base_data.json') as json_file:
                    data2 = json.load(json_file)
                dct = data2
                if not dct['TIER_LISTS'].get(key):
                    dct['TIER_LISTS'][key] = {
                        'Intensities': [],
                        'Replace_Value': ''
                    }
                if len(data['TIER_LISTS'][key]) > Max_Intensity:
                    dct['TIER_LISTS'][key]['Intensities'] = None
                else:
                    dct['TIER_LISTS'][key]['Intensities'] = data['TIER_LISTS'][key]
            except:

                if not dct['TIER_LISTS'].get(key):
                    dct['TIER_LISTS'][key] = {
                        'Intensities': [],
                        'Replace_Value': ''
                    }

                if len(data['TIER_LISTS'][key]) > Max_Intensity:
                    dct['TIER_LISTS'][key]['Intensities'] = None
                else:
                    dct['TIER_LISTS'][key]['Intensities'] = data['TIER_LISTS'][key]

            with open('base_data.json', 'w') as json_file:
                json.dump(dct, json_file, indent=4)

            dct = {}
        else:
            try:
                with open('base_data.json') as json_file:
                    data3 = json.load(json_file)
                    lst_select = data3['TIER_LISTS'].keys()
                    dct1 = data3

                if key in lst_select:
                    del dct1['TIER_LISTS'][key]
                with open('base_data.json', 'w') as json_file:
                    json.dump(dct1, json_file, indent=4)
            except:
                False

            dct1 = {}

        if key in replace_choice:
            try:
                with open('base_data.json') as json_file:
                    data2 = json.load(json_file)
                dct = data2
                if not dct['TIER_LISTS'].get(key):
                    dct['TIER_LISTS'][key] = {
                        'Intensities': [],
                        'Replace_Value': ''
                    }
                value = checkbox_state[f"{key}_replace"]

                if len(data['TIER_LISTS'][key]) > Max_Intensity:
                    dct['TIER_LISTS'][key]['Intensities'] = None
                dct['TIER_LISTS'][key]['Replace_Value'] = value
            except:
                0

            with open('base_data.json', 'w') as json_file:
                json.dump(dct, json_file, indent=4)

            dct = {}

        else:
            try:
                with open('base_data.json') as json_file:
                    data3 = json.load(json_file)
                    lst_select = data3['TIER_LISTS'].keys()
                    dct2 = data3

                if key in lst_select:
                    dct2['TIER_LISTS'][key]['Replace_Value'] = ''
                with open('base_data.json', 'w') as json_file:
                    json.dump(dct2, json_file, indent=4)
            except:
                False

            dct2 = {}

    return no_update
