from dash import html

def page_container(title, children, **kwargs):
    return html.Div(className="flex flex-col gap-12 max-w-2xl", children=[
        html.H1(title, className="text-3xl font-bold"),
        html.Div(className="flex flex-col gap-8", children=children, **kwargs)
    ])