import subprocess
import streamlit as st
import os, sys, json
import Affichage_pattern
import hashlib
Affichage_pattern.affichage()
script_path = os.path.realpath(os.path.dirname("src"))
os.chdir(script_path)
sys.path.append("..")
from src.snl_stats_extraction_data import get_parameters
def page7():

    DIR, databases_pair_paths, databases_paths, tier_lists, databases, databases_pairs, tiers=get_parameters()

    def initialize_checkbox_state():
        checkbox_state = st.experimental_get_query_params().get("checkbox_state", [None])[0]
        if checkbox_state:
            checkbox_state = json.loads(checkbox_state)
        else:
            checkbox_state = {}
        return checkbox_state

    def update_query_params(checkbox_state):
        checkbox_state_json = json.dumps(checkbox_state)
        checkbox_hash = hashlib.md5(checkbox_state_json.encode()).hexdigest()
        st.experimental_set_query_params(checkbox_state=checkbox_state_json, hash=checkbox_hash)
        
    checkbox_state = initialize_checkbox_state()
    checkboxes = {}
    i = 0
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("TIERS")
    with col2:
        st.subheader("Valid TIERS for data analysis")
    with col3:
        st.subheader("Replace Value")

    # Création des cases à cocher pour chaque label
    input_key_Intensity = f"Max_Intensity"
    st.markdown('''Select a maximum of intensity for a tier to be considered without Replace_Value''')
    Number_input = checkbox_state.get(input_key_Intensity, 25)
    Max_Intensity = st.number_input(label= "Select Value", value=Number_input, key=input_key_Intensity)
    checkbox_state[input_key_Intensity] = Max_Intensity

    update_query_params(checkbox_state)

    lst_choice = []
    replace_choice = []
    for label in tier_lists.keys():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(label)
        with col2:
            checkbox_key = f"{label}_tag"
            checkbox_value = checkbox_state.get(checkbox_key, False)
            checkbox_value = st.checkbox("Validate", value=checkbox_value, key=checkbox_key)
            checkbox_state[checkbox_key] = checkbox_value
        i += 1

        with col3:
            replace_value_key = f"{label}_replace"
            replace_value = checkbox_state.get(replace_value_key, "")
            replace_value = st.text_input("Replace Value", value=replace_value, key=replace_value_key)
            checkbox_state[replace_value_key] = replace_value
        i += 1

    update_query_params(checkbox_state)

    for label in checkbox_state.keys(): 
        option1_checked = checkbox_state[label]
        if option1_checked == True:
            lst_choice.append(label.replace('_tag',''))

        if option1_checked == False:
            if label in lst_choice:
                lst_choice.remove(label.replace('_tag',''))
        
        if option1_checked != False and option1_checked != True :

            if option1_checked :

                replace_choice.append(label.replace('_replace',''))
            
            else :

                if label.replace('_replace','') in replace_choice :

                    replace_choice.remove(label.replace('_tag',''))

    with open('data.json') as json_file:
        data = json.load(json_file)
    dct = {}
    dct['TIER_LISTS'] = {}

    for key in data['TIER_LISTS'].keys():
        if key in lst_choice:
            try:
                with open('base_data.json') as json_file:
                    data2 = json.load(json_file)  
                dct = data2
                if not dct['TIER_LISTS'].get(key):
                    dct['TIER_LISTS'][key] = {
                        'Intensities': [],
                        'Replace_Value': ''
                    }
                if len(data['TIER_LISTS'][key]) > Max_Intensity :
                    dct['TIER_LISTS'][key]['Intensities'] = None
                else :
                    dct['TIER_LISTS'][key]['Intensities'] = data['TIER_LISTS'][key]
            except:

                if not dct['TIER_LISTS'].get(key):
                    dct['TIER_LISTS'][key] = {
                        'Intensities': [],
                        'Replace_Value': ''
                    }

                if len(data['TIER_LISTS'][key]) > Max_Intensity :
                    dct['TIER_LISTS'][key]['Intensities'] = None
                else :
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
        
        if key in replace_choice :
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

                if len(data['TIER_LISTS'][key]) > Max_Intensity :
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

            


    update_query_params(checkbox_state)

page7()