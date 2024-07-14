import dash_mantine_components as dmc
from dash import html


def slider(id, value=None, minimum=0, maximum=100, label=None, step=1):
    if value is None:
        value = minimum
    return html.Div([
        html.Span(children=label, className="text-sm font-medium"),
        dmc.Slider(
            id=id,
            min=minimum,
            max=maximum,
            value=value,
            labelAlwaysOn=True,
            classNames={
                "label": "bg-transparent p-0 -top-6 text-black",
                "track": "before:bg-gray-100",
            },
            step=step,
            marks=[
                {"value": minimum, "label": f"{minimum}"},
                {"value": int((maximum - minimum) / 2), "label": f"{int((maximum - minimum) / 2)}"},
                {"value": maximum, "label": f"{maximum}"},
            ],
        ),
    ], className="flex flex-col gap-6 mb-4")


