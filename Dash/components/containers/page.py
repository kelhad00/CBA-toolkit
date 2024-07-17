from dash import html, dcc, callback, Input, Output



def page_container(children, **kwargs):
    return html.Div(className="flex flex-col gap-8", children=children)


