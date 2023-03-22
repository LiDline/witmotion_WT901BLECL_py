import dash_bootstrap_components as dbc
from dash import dcc
from dash_extensions.enrich import html


def drop_menu():
    dropdown = dcc.Dropdown(
        options=[], id='dropdown', placeholder='Select...', disabled=True
    )
    text = dbc.FormText("Choice device address here...")
    return html.Div([dropdown, text])
