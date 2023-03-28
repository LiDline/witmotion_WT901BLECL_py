import dash_bootstrap_components as dbc
from dash import dcc
from dash_extensions.enrich import html


def drop_menu():
    dropdown = dcc.Dropdown(
        options=[], id='dropdown', placeholder='Select...', disabled=True
    )
    text = dbc.FormText("Choice device address here...")
    return html.Div([dropdown, text])

# Частота считывания
def rate():
    dropdown = dcc.Dropdown(
        options=[0.2, 0.5, 1, 2, 5, 10 , 20, 50], value=10, id='rate', placeholder='Select...', disabled=False
    )
    text = dbc.FormText("Choice reading rate [Hz] here...")
    return html.Div([dropdown, text])
