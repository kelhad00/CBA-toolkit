import dash
from dash import Dash, html, dcc, Output, Input
import dash_mantine_components as dmc

external_scripts = [
    {'src': 'https://cdn.tailwindcss.com'}
]

app = Dash(__name__, use_pages=True, external_scripts=external_scripts)


def nav_section(title, pages):
    return html.Div(className="nav-section-container", children=[
        html.H2(className="nav-title", children=title),
        html.Div(className="nav-section", children=[
            dcc.Link( href=page["relative_path"], className=f"nav-item-{page['active']}", children=[
                html.Div(className="nav-item-icon", children=""),
                html.Span(f"{page['name']}", className="nav-link"),
            ]) for page in pages
        ])
    ])

@app.callback(
    Output('nav-section-container', 'children'),
    Input('url', 'pathname')
)
def update_nav_section(pathname):
    return html.Div(className="h-full flex gap-8", children=[
        html.Div(className="flex flex-col justify-between h-full w-52", children=[
            html.Div(className="nav", children=[
                html.H1(children='CBA Toolkit', className="text-3xl font-bold"),
                nav_section("Dashboard", [
                    {"name": "Home", "relative_path": "/", "active": "/" == pathname},
                    {"name": "Description", "relative_path": "/description/", "active": "/description/" == pathname},
                    {"name": "Durations", "relative_path": "/durations", "active": "/durations" == pathname},
                    {"name": "Effects", "relative_path": "/effects", "active": "/effects" == pathname},
                ]),
                nav_section("Configuration", [
                    {"name": "Datasets", "relative_path": "/datasets", "active": "/datasets" == pathname},
                    {"name": "Tiers", "relative_path": "/tiers", "active": "/tiers" == pathname},
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
            html.Div(style={'width': '100%'}, children=[
                dash.page_container
            ]),
        ], className="""h-screen flex gap-8 p-8 """)
    ]
)

if __name__ == '__main__':
    app.run(debug=True)