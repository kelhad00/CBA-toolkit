import dash
from dash import Dash, html, dcc, Output, Input
import dash_mantine_components as dmc

from Dash.assets.icons.Database import database_search_icon
from Dash.assets.icons.Home import home_icon
from Dash.assets.icons.Information import information_icon
from Dash.assets.icons.Tier import tier_icon
from Dash.assets.icons.Time import time_icon
from Dash.assets.icons.Effect import effect_icon


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
                    {"name": "Durations", "relative_path": "/durations/intra", "active": "/durations" in pathname, "icon": time_icon},
                    {"name": "Effects", "relative_path": "/effects", "active": "/effects" in pathname, "icon": effect_icon},
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
                dash.page_container
            ]),
        ], className="h-screen flex gap-8 px-8")
    ]
)

if __name__ == '__main__':
    app.run(debug=True)