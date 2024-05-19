import dash
from dash import html
import dash_mantine_components as dmc

from Dash.components.containers.page import page_container

dash.register_page(__name__, path='/')

layout = page_container("Home", [
    dmc.Text("Uncover the Secrets of Communication with Conversational Behavior Analysis!"),
    dmc.Text("Revolutionizing the way you analyze nonverbal cues in conversations, our tool provides you with unprecedented insights into human interactions."),
    dmc.Text("Say goodbye to superficial analysis! Go beyond the words and decipher the true intentions and emotions of conversation participants with our powerful tool."),
    dmc.Text("Clear and precise graphs allow you to visualize in real time the facial expressions, body language, and tone of voice of each speaker."),
    dmc.Text("Perfectly suited for a multitude of contexts, our tool will be invaluable to you for:"),
    dmc.List([
        dmc.ListItem("Improving communication in businesses, training, coaching, or therapy."),
        dmc.ListItem("Resolving conflicts by identifying sources of tension and facilitating dialogue."),
        dmc.ListItem("Strengthening interpersonal relationships by better understanding the needs and emotions of those around you."),
        dmc.ListItem("Optimizing recruitment by evaluating candidates in a more detailed and objective way."),
    ]),
    dmc.Text("Empower yourself with an indispensable asset to better understand the subtleties of human communication!"),
    dmc.Text("Try our tool today and discover a world of new possibilities."),
])