from dash import html, callback, Output, Input

def section_container(title, description, children, id="", **kwargs):
    return html.Div(className="flex flex-col gap-4", children=[
        html.Div([
            html.H2(title, className="text-2xl font-medium"),
            html.Span(description, id="span-description_pages", className="text-sm font-light"),
        ], className="flex flex-col"),
        html.Div(className="flex flex-col gap-4", children=children, id=id)
    ], **kwargs)


@callback(
    Output('span-description_pages', 'style'),
    Input('span-description_pages', 'children'),
)
def update_output(value):
    if value != "":
        return {'display': 'block'}
    else:
        return {'display': 'none'}



def sub_section_container(title, description, children, id="", **kwargs):
    return html.Div(className="flex flex-col gap-4 pt-4", children=[
        html.Div([
            html.H3(title, className="text-lg font-medium"),
            html.Span(description, id="span-description_pages", className="text-sm font-light"),
        ], className="flex flex-col"),
        html.Div(className="flex flex-col gap-4", children=children, id=id)
    ], **kwargs)