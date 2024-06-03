import dash
from dash import Dash, html, dcc, Output, Input
import dash_mantine_components as dmc

from Dash.assets.icons.Database import database_search_icon
from Dash.assets.icons.Home import home_icon
from Dash.assets.icons.Information import information_icon
from Dash.assets.icons.Link import link_icon
from Dash.assets.icons.Mimicry import mimicry_icon
from Dash.assets.icons.Tier import tier_icon
from Dash.assets.icons.Time import time_icon
from Dash.assets.icons.Effect import effect_icon
from Dash.components.containers.page import page_container
from Dash.components.interaction.segment import segment

external_scripts = [
    {'src': 'https://cdn.tailwindcss.com'}
]

app = Dash(__name__, use_pages=True, external_scripts=external_scripts, suppress_callback_exceptions=True)


def nav_section(title, pages):

    return html.Div(className="nav-section-container", children=[
        html.H2(className="nav-title", children=title),
        html.Div(className="nav-section", children=[
            dcc.Link( href=page["relative_path"], className=f"nav-item-{page['active']}", children=[
                page['icon'](color='white' if page['active'] else 'black', width="24px"),
                html.Span(f"{page['name']}", className="nav-link"),
            ]) for page in pages
        ])
    ])

@app.callback(
    Output('nav-section-container', 'children'),
    Input('url', 'pathname')
)
def update_nav_section(pathname):
    return html.Div(className="h-full py-8 flex gap-8", children=[
        html.Div(className="flex flex-col justify-between h-full w-52", children=[
            html.Div(className="nav", children=[
                html.H1(children=['CBA', html.Span('Toolkit', className="font-medium text-gray-500")], className="text-3xl font-bold"),
                nav_section("Dashboard", [
                    {"name": "Home", "relative_path": "/", "active": "/" == pathname, "icon": home_icon},
                    {"name": "Description", "relative_path": "/description/", "active": "/description/" in pathname, "icon": information_icon},
                    {"name": "Durations", "relative_path": "/duration/intra", "active": "/duration" in pathname, "icon": time_icon},
                    {"name": "Tracking", "relative_path": "/tracking", "active": "/tracking" in pathname, "icon": effect_icon},
                    {"name": "Mimicry", "relative_path": "/mimicry", "active": "/mimicry" in pathname, "icon": mimicry_icon},
                    {"name": "Correlation", "relative_path": "/correlation", "active": "/correlation" in pathname, "icon": link_icon},

                ]),
                nav_section("Configuration", [
                    {"name": "Datasets", "relative_path": "/datasets", "active": "/datasets" in pathname, "icon": database_search_icon},
                    {"name": "Tiers", "relative_path": "/tiers", "active": "/tiers" in pathname, "icon": tier_icon},
                ]),
            ]),
        ]),
        html.Hr(className="h-full border-l-2 border-gray-200"),
    ])




app.layout = dmc.MantineProvider(
    theme={
        "primaryColor": "dark",
    },
    children=[
        html.Div(children=[
            dcc.Location(id='url', refresh=False),
            html.Div(id='nav-section-container'),
            html.Div(className="w-full h-full overflow-y-scroll p-8", children=[
                html.Div(className="flex flex-col gap-12 max-w-3xl", children=[
                    html.Div(className="flex gap-8 justify-between items-center flex-wrap", children=[
                        html.H1(className="text-3xl font-bold", id="page-title"),
                        html.Div(id='segment'),
                    ]),
                    dash.page_container
                ]),
            ]),
        ], className="h-screen flex gap-8 px-8")
    ]
)


def get_title(url, options):
    for option in options:
        if option["href"] == "/":
            if option["href"] == url:
                return option["label"]
        else:
            if option["href"] in url:
                return option["label"]
    return "Page not found"


@app.callback(
    Output("page-title", "children"),
    Input("url", "pathname"),
)
def update_page_title(url):
    options = [
        {"label": "Description", "href": "/description/"},
        {"label": "Home", "href": "/"},
        {"label": "Tiers", "href": "/tiers"},
        {"label": "Datasets", "href": "/datasets"},
        {"label": "Tracking", "href": "/tracking"},
        {"label": "Durations", "href": "/duration/"},
        {"label": "Mimicry", "href": "/mimicry"},
        {"label": "Correlation", "href": "/correlation"},
    ]

    return get_title(url, options)

@app.callback(
    Output('segment', 'children'),
    Input('url', 'pathname')
)
def update_segment(pathname):

    description = [
        {"label": "General", "href" : "/description/", "active": "/description/" == pathname},
        {"label": "Expressions/Minute", "href": "/description/per_minute", "active": "/description/per_minute" in pathname},
        {"label": "Statistics", "href": "/description/stats", "active": "/description/stats" in pathname},
    ]

    durations = [
        {"label": "Intra", "href": "/duration/intra", "active": "/duration/intra" in pathname},
        {"label": "Inter", "href": "/duration/inter", "active": "/duration/inter" in pathname},
    ]

    if "/description" in pathname:
        return segment(description)
    elif "/duration" in pathname:
        return segment(durations)
    else:
        return None






if __name__ == '__main__':
    app.run(debug=True)