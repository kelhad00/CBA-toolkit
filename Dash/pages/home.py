import dash
from dash import html, dcc
import dash_mantine_components as dmc

from Dash.components.containers.page import page_container
from Dash.components.containers.section import section_container
from Dash.components.containers.page import page_container


dash.register_page(__name__, path='/')

layout = page_container(children=[
    section_container("Uncover the Secrets of Communication with Conversational Behavior Analysis!", description="", children=[
        html.Span(
            "Revolutionizing the way you analyze nonverbal cues in conversations, our tool provides you with unprecedented insights into human interactions.",
            className="font-light"
        ),
    ]),
    section_container("Say goodbye to superficial analysis!", description="", children=[
        html.Span(
            "Go beyond the words and decipher the true intentions and emotions of conversation participants with our powerful tool.",
            className="font-light"
        ),
        html.Span(
            "Clear and precise graphs allow you to visualize in real time the facial expressions, body language, and tone of voice of each speaker.",
            className="font-light"
        ),
    ]),
    dcc.Link(
        href="/datasets",
        children=[
            dmc.Button(html.Span(className="font-normal", children="Get started !"), radius="md"),
        ]
    )



])

#     dmc.Text("Go beyond the words and decipher the true intentions and emotions of conversation participants with our powerful tool."),

# ]))
