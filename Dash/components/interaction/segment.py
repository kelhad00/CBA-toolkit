from dash import html, dcc
import dash_mantine_components as dmc


def segment_item(href, label, active):
    style = "rounded-lg px-4 py-2 text-xs transition-all duration-250 hover:bg-gray-100"
    if active :
        style = "bg-black rounded-lg px-4 py-2 text-white text-xs transition-all duration-250"
    return dcc.Link(
        href=href,
        className=style,
        children=label
    )

def segment(options):
    return html.Div(children=[
        html.Div([segment_item(option["href"], option["label"], option["active"]) for option in options], className="border-gray-100 border flex p-0.5 w-fit rounded-xl"),
    ])


