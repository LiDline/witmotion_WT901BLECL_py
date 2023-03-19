import dash_bootstrap_components as dbc
from dash_extensions.enrich import html


def input_address():
    text_input = html.Div([
        dbc.Input(id="input", placeholder="/dev/ttyUSB0 or COM3", value="/dev/ttyUSB0", type="text"),
        dbc.FormText("Insert device address here..."),
        ])
    return text_input