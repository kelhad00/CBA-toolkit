import dash
from dash import html, dcc, callback, Input, Output, State, no_update
from dash.dependencies import ALL
import os
import zipfile
import base64
import io
import shutil
import ast

from Dash.assets.icons.Delete import delete_icon
from Dash.components.interaction.table import table_line, table_cell, table_container
from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container


dash.register_page(__name__)


def display_directories():
    relative_path = os.path.join("..", "data")
    path = os.path.abspath(relative_path)
    entries = os.listdir(path)
    directories = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
    nb_files_directories = [len(os.listdir(os.path.join(path, directory))) for directory in directories]
    return [display_table_line(directory, nb_files) for directory, nb_files in zip(directories, nb_files_directories)]


def display_table_line(file_name, nb_files):
    return table_line([
        table_cell("name", file_name),
        table_cell("files", nb_files),
        html.Div(className="cursor-pointer", id={'type': 'delete-button', 'index': file_name}, children=[
            delete_icon("white", "24px"),
        ]),
    ])



layout = page_container("Datasets", [
    section_container("Import Dataset","" ,[
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
    ctx = dash.callback_context
    input = ctx.triggered[0]['prop_id']
    print("triggered" + str(input))
    if input == 'url.pathname' or input == 'output-data-upload.children':
        return display_directories() if pathname or upload_children else no_update

    else:
        if n_clicks is not None and 1 in n_clicks:
            # Find the index of the button that was clicked
            index = n_clicks.index(1)
            # Get the file_name associated with the clicked button
            file_name = ids[index]['index']
            print(file_name)
            # Call the function you want to execute
            delete_dataset_uploaded(file_name)
        return display_directories()


@callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is not None:
        # Split the 'contents' into the data type and the base64 encoded data
        content_type, content_string = contents.split(',')

        # Decode the base64 string
        decoded = base64.b64decode(content_string)

        # Use BytesIO to handle the decoded content as a file
        file = io.BytesIO(decoded)

        file_name = filename.split(".")[0]
        relative_path = os.path.join("..", "data")
        path = os.path.abspath(relative_path)
        if not os.path.exists(path):
            # Creation of the directory
            os.makedirs(path)
        with zipfile.ZipFile(file, "r") as zip_ref:
            files = zip_ref.namelist()

            only_files = [f for f in files if not zip_ref.getinfo(f).is_dir()]
            subfolders = [f for f in files if zip_ref.getinfo(f).is_dir()]
            split_subfolders = []
            for folder in subfolders:
                folder_path = os.path.normpath(folder)
                split_subfolders.append(os.path.split(folder_path)[-1])
            for folder in split_subfolders:
                os.makedirs(os.path.join(path, folder), exist_ok=True)
            eaf_files = []
            for file in only_files:
                if file.endswith(".eaf"):
                    eaf_files.append(file)

            print(subfolders)
            print(split_subfolders)

            if 'IB' in split_subfolders:
                split_subfolders.remove('IB')

            # delete IB/.DS_Store in the zip file with os
            if 'IB/.DS_Store' in only_files:
                only_files.remove('IB/.DS_Store')

            if len(eaf_files) == 0 or len(eaf_files) != len(only_files):
                return "Invalid directory"

            zip_ref.extractall(path)
            for folder in split_subfolders:
                doss = os.path.join(path, file_name)
                print(doss)
                doss2 = os.path.join(doss, folder)
                print(doss2)
                for file2 in os.listdir(doss2):
                    src_path = os.path.join(doss2, file2)
                    destination_path = os.path.join(os.path.join(path, folder), file2)

                    print(src_path)
                    print(destination_path)
                    # Verification if the file is a file (and not a subfolder)
                    if os.path.isfile(src_path):
                        shutil.move(src_path, destination_path)
            if split_subfolders:
                shutil.rmtree(os.path.join(path, file_name))
            dataset_name = file_name
            add_form_pairs_function(dataset_name)
        return html.Div([
            '✅File Name: ' + file_name,
        ])

def add_form_pairs_function(dataset_name):
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
    try:
        relative_path = os.path.join("..", "data")
        path = os.path.abspath(relative_path)
        path_dataset_to_delete = os.path.join(path, dataset_name)
        print(path_dataset_to_delete)
        shutil.rmtree(path_dataset_to_delete)
    except:
        print("No database uploaded")






