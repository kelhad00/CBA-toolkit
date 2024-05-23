import dash_mantine_components as dmc
from dash import html

def accordion(children, multiple=False, value=None):
    if multiple:
        return dmc.AccordionMultiple(
            children=children,
            radius="md",
            value=value,
            classNames={
                "label": "font-medium text-lg px-0",
                "content": "flex flex-col gap-4 pb-8",
            }
        )
    else:
        return dmc.Accordion(
            children=children,
            radius="md",
            value=value,
            classNames={
                "label": "font-medium text-lg px-0",
                "content": "flex flex-col gap-4 pb-8",

            }
        )

def accordion_item(children, label, value, description=None):
    return dmc.AccordionItem([
            dmc.AccordionControl(
                html.Div(
                    [
                        dmc.Text(label),
                        dmc.Text(description, size="xs", fw=400, c="dimmed"),
                    ]
                ), className="rounded-md "
            ),
            dmc.AccordionPanel(children=children,className="flex flex-col gap-4")
        ],
        value=value,
    )


