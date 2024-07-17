import dash
from dash import html, dcc, callback, Input, Output, State, no_update
from dash.dependencies import ALL
import dash_mantine_components as dmc

import os
import zipfile
import base64
import io
import shutil
import ast
import keyword


from Dash.components.interaction.table import table_line, table_cell, table_container
from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container

from Dash.assets.icons.Delete import delete_icon
from src.json_creation import create_json_from_directory

dash.register_page(__name__)


def sanitize_function_name(name):
    valid_chars = []
    for char in name:
        if char.isalnum() or char == "_":
            valid_chars.append(char)
    sanitized_name = ''.join(valid_chars)
    if keyword.iskeyword(sanitized_name):
        sanitized_name += "_"
    return sanitized_name



def display_directories():
    """ Display the directories in the data folder.
    Return:
        list : list of table line that contains the directories.
    """
    relative_path = os.path.join("..", "data")
    path = os.path.abspath(relative_path)
    try:
        entries = os.listdir(path)
    except:
        entries = []
    directories = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
    nb_files_directories = [len(os.listdir(os.path.join(path, directory))) for directory in directories]
    return [display_table_line(directory, nb_files) for directory, nb_files in zip(directories, nb_files_directories)]


def display_table_line(file_name, nb_files):
    """ Display a table line for a directory.
    Params:
        file_name: The name of the directory.
        nb_files: The number of files in the directory.
    Return:
        html.Div : A table line.
    """
    return table_line([
        table_cell("name", file_name),
        table_cell("files", nb_files),
        html.Div(className="cursor-pointer", id={'type': 'delete-button', 'index': file_name}, children=[
            delete_icon("white", "24px"),
        ]),
    ])


layout = page_container(children=[
    section_container("Import Dataset", "Add new files to analyze", [
        dcc.Upload(
            id='upload-data',
            accept='.zip',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            className="flex items-center justify-center w-full h-64 bg-gray-100 border-2 border-dashed border-gray-300 rounded-md cursor-pointer",
        ),
        html.Div(id='output-data-upload'),
    ]),
    section_container("All Datasets", "", [
        table_container(children=display_directories(), id="directory-list"),
    ]),
    section_container("Paring functions", "Add paring function to analyze the interaction between multiple characters", [
        dmc.Alert(
           html.Div(className="flex flex-col gap-2", children=[
               html.Span("Here upload your own function(s) to configure the paring of the interaction in order to explore your dataset. "
                         "It only must be done if the way of naming the eaf files by interaction pairs is different from 'A_1_...' & 'B_1_...'."),
               html.Span("The function must be named 'form_pairs_(dataset_name)' and must take a list of filenames as input and return a list of pairs of filenames." ),
           ]),
            title="Explanation",
            color="gray",
        ),
        dcc.Upload(
            id='upload-paring',
            accept='.py',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            className="flex items-center justify-center w-full h-64 bg-gray-100 border-2 border-dashed border-gray-300 rounded-md cursor-pointer",
        ),
        html.Div(id='output-paring-upload'),

        dmc.Alert(
            title="Example",
            color="gray",
            children=dmc.Prism(
                """# Example of a paring function for CCDB dataset
def form_pairs_ccdb(lst):
    '''Return filename pairs [(), (), ...].
    Args:
        lst (list): list of filenames without the path.
    Returns:
        list: [(),(),...].
    '''
    final = []
    replace_with = {'dizzy': 'monk', 'monk': 'dizzy'}
    i = 0
    while i < len(lst):
        key = lst[i].split('_')[-1].split('.')[0]
        pair = lst[i].replace(key, replace_with[key])
        if pair in lst:
            final.append((lst[i], pair))
            lst.remove(lst[i])
            lst.remove(pair)
        else:
            i = +1
    for l in lst:
        continue
    return final""",
                language="python",
            ),
        )
    ]),

])


@callback(
    Output('directory-list', 'children'),
    [Input({'type': 'delete-button', 'index': ALL}, 'n_clicks'),
     Input('url', 'pathname'),
     Input('output-data-upload', 'children')],
    [State({'type': 'delete-button', 'index': ALL}, 'id'),
     State('directory-list', 'children')],
)
def update_directory_list(n_clicks, pathname, upload_children, ids, current_children):
    # Determine the input that triggered the callback
    ctx = dash.callback_context
    input = ctx.triggered[0]['prop_id']

    # if Routing or upload of a new dataset
    if input == 'url.pathname' or input == 'output-data-upload.children':
        if pathname or upload_children:
            return display_directories()
        else:
            return no_update

    else:
        if n_clicks is not None and 1 in n_clicks:
            # Find the index of the button that was clicked
            index = n_clicks.index(1)
            # Get the file_name associated with the clicked button
            file_name = ids[index]['index']
            delete_dataset_uploaded(file_name)
        return display_directories()


@callback(
    Output('output-paring-upload', 'children'),
    Input('upload-paring', 'contents'),
    State('upload-paring', 'filename')
)
def update_output(contents, filename):
    if contents is not None:
        # Split the 'contents' into the data type and the base64 encoded data
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        file = io.BytesIO(decoded)
        content = file.read()

        try:
            tree = ast.parse(content)
        except:
            return "Invalid file. Please upload a valid python file."

        try:
            relative_path = os.path.join("..", "IBPY")
            file_path = os.path.join(relative_path, "db.py")
            path = os.path.abspath(file_path)

            with open(path, 'r') as f_destination:
                code_destination = f_destination.read()
                tree_destination = ast.parse(code_destination)
        except:
            return "No db.py file found."

        if tree and tree_destination:
            try:
                functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                functions_destination = [node.name for node in ast.walk(tree_destination) if isinstance(node, ast.FunctionDef)]
                print(functions)

                duplicates_between_files = set(functions) & set(functions_destination)

                # check if the function is named correctly
                if not functions or not all([f.startswith("form_pairs_") for f in functions]):
                    print(functions)
                    return "Invalid function name. Please upload a function named 'form_pairs_(dataset_name)'."

                # check if some functions have the same name
                if len(set(functions)) != len(functions):
                    return "Invalid function name. Please upload a function with a unique name."

                # Remove existing function from AST
                if duplicates_between_files:
                    for node in ast.walk(tree_destination):
                        if isinstance(node, ast.FunctionDef) and node.name in duplicates_between_files:
                            tree_destination.body.remove(node)

                with open(path, 'w') as f_destination:
                    f_destination.write(ast.unparse(tree_destination))
                    f_destination.write("\n")
                    f_destination.write("\n")
                    f_destination.write(content.decode("utf-8"))

                return html.Div([
                    '✅File Name: ' + str(functions),
                ])

            except Exception as e:
                print(e)
                return "Error while updating the db.py file."


@callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is not None:
        # Split the 'contents' into the data type and the base64 encoded data
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        file = io.BytesIO(decoded)

        relative_path = os.path.join("..", "data")
        path = os.path.abspath(relative_path)
        if not os.path.exists(path):
            os.makedirs(path)

        with zipfile.ZipFile(file, "r") as zip_ref:
            files = zip_ref.namelist()
            only_files = [f for f in files if not zip_ref.getinfo(f).is_dir()]
            eaf_files = [file for file in only_files if file.endswith(".eaf")]
            zip_ref.extractall(path)

        # Get the absolute path of the extracted files
        eaf_files = [os.path.join(path, eaf_file) for eaf_file in eaf_files]

        # order the datasets in the data folder
        datasets = order_datasets(eaf_files, path)

        for dataset in datasets:
            dataset = os.path.split(dataset)[-1]

            # rename dataset that are not valid python variable names
            if not dataset.isidentifier():
                folder_correct = sanitize_function_name(dataset)
                os.rename(os.path.join(path, dataset), os.path.join(path, folder_correct))
                dataset = folder_correct

            # add a form_pairs function to the db.py file
            add_form_pairs_function(dataset)

        create_json_from_directory()
        return html.Div([
            '✅Successfully uploaded dataset(s)',
        ])


def order_datasets(eaf_files, path):
    '''
    Order the datasets in the data folder. we only keep the eaf files in the dataset folder (the parent dir).
    Args:
        eaf_files:
        path:

    Returns:
        set of datasets
    '''
    datasets = set()

    # move eaf files to the dataset folder
    for eaf_file in eaf_files:
        parent_folder = os.path.dirname(eaf_file).split("/")[-1]
        dataset_folder = os.path.join(path, parent_folder)
        os.makedirs(dataset_folder, exist_ok=True)
        datasets.add(dataset_folder)

        if os.path.dirname(eaf_file) != dataset_folder:
            # check if the file already exists in the folder
            if not os.path.isfile(os.path.join(dataset_folder, os.path.basename(eaf_file))):
                shutil.move(eaf_file, dataset_folder)

    # delete empty folders
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        if folder_path not in datasets:
            # check if the folder is empty of eaf files
            if not any(file.endswith(".eaf") for file in os.listdir(folder_path)):
                shutil.rmtree(folder_path)

    return datasets

def add_form_pairs_function(dataset_name):
    """Add a form_pairs function to the db.py file.
    Args:
        dataset_name (str): name of the dataset.
    """
    relative_path = os.path.join("..", "IBPY")
    db_py_path = os.path.join(relative_path, "db.py")

    form_pairs_code = f'''
def form_pairs_{dataset_name}(lst):
    """Return filename pairs [(), (), ...].

    Args:
        lst (list): list of filenames without the path.
    Returns:
        list: [(), (), ...].
    """
    pairs = form_pairs_ab(lst)
    return pairs
'''

    # Load contents of db.py file
    with open(db_py_path, "r") as file:
        content = file.read()

    # Analyze the source code of the file
    tree = ast.parse(content)

    # Check if function already exists
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == f"form_pairs_{dataset_name}":
            print("The function already exists.")
            return

    # Create AST for the new function
    new_tree = ast.parse(form_pairs_code)
    new_function_def = new_tree.body[0]
    new_function_def.name = f"form_pairs_{dataset_name}"

    # Add function to existing AST
    tree.body.append(new_function_def)

    # Convert the modified AST to text
    modified_code = ast.unparse(tree)

    # Write the modified code back to db.py file
    with open(db_py_path, "w") as file:
        file.write(modified_code)
    print(f"The form_pairs_{dataset_name} function was successfully added.")



def delete_dataset_uploaded(dataset_name):
    """Delete the dataset uploaded.
    Args:
        dataset_name (str): name of the dataset.
    """
    try:
        relative_path = os.path.join("..", "data")
        path = os.path.abspath(relative_path)
        path_dataset_to_delete = os.path.join(path, dataset_name)
        shutil.rmtree(path_dataset_to_delete)
        create_json_from_directory()
    except:
        print("No database uploaded")






