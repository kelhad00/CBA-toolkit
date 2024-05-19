from dash import html, dcc

def page_container(title, children, **kwargs):
    return html.Div(className="flex flex-col gap-12 max-w-2xl", children=[
        html.Div(className="flex gap-8 justify-between items-center flex-wrap", children=[
            html.H1(title, className="text-3xl font-bold"),
            html.Div(
                # className="flex justify-center",
                children=[
                    html.Div([
                        dcc.Link(href="/description/", className="bg-black rounded-lg px-4 py-2 text-white text-xs",
                                 children="General"),
                        dcc.Link(href="/description/per_minute",
                                 className="rounded-lg px-4 py-2 hover:bg-gray-500 text-xs",
                                 children="Expressions/Minute"),
                        dcc.Link(href="/description/stats", className=" rounded-lg px-4 py-2 hover:bg-gray-500 text-xs",
                                 children="Statistics")
                    ],
                        className="border-gray-100 border flex p-1 w-fit rounded-xl"
                    ),
                ]
            ),
        ]),
        html.Div(className="flex flex-col gap-8", children=children, **kwargs)
    ])