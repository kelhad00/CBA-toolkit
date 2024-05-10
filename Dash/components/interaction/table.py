from dash import html


def table_container(children, **kwargs):
    return html.Div(className="table-container", children=children, **kwargs)

def table_line(children, **kwargs):
    return html.Div(className="table-line", children=children, **kwargs)


def table_cell(label, children, **kwargs):
    return html.Div(className="flex-1 flex flex-col", children=[
        html.Span(label + " :", className="text-sm font-light"),
        children
    ])



