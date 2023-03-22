from dash_extensions import WebSocket
from dash_extensions.enrich import html, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash
import re
import os
import requests
import json


from func.func_dash.app_content import header_page
from func.func_dash.drop_menu import drop_menu
from func.func_dash.inputs import input_address
from func.func_dash.buttons import connection, start
from func.counter import Counter


dash.register_page(__name__)
# ___________________________________________________________________________________________________

# Client-side function (for performance) that updates the graph.
with open('func/graph.js') as f:    # plot the data
    update_graph = f.read()
# ___________________________________________________________________________________________________

'''layout'''

layout = html.Div([
    # Websocket
    WebSocket(id="ws", url="ws://127.0.0.1:5000/ws"),

    # Header
    dbc.Row([
            dbc.Col([
                header_page(re.sub(r'\w+\.', '', __name__)),
            ])
            ], className='other'),
    # DropdownMenu and Button "Connections"
    dbc.Row([
        dbc.Col([
            drop_menu()
        ], width={"size": 2}),
        dbc.Col([
            connection()
        ]),
        dbc.Col([
            html.Div(id='message_from_server')
        ])
    ], className='other'),
    dbc.Row([]),
])
# ___________________________________________________________________________________________________

'''Callback'''    

# Обновление поля Selected
@dash.callback(
    Output('dropdown', 'disabled'),
    Output('dropdown', 'options'),
    Input('button_search', 'n_clicks'),
    prevent_initial_call=True,
)
def disabled(bt1):
    ports = requests.get('http://127.0.0.1:5001/available_ports').json()
    return [False, ports]

# Активация|деактивация кнопки Connection
@dash.callback(
    Output('button_connection', 'disabled'),
    Input('dropdown', 'value'),
    prevent_initial_call=True,
)
def disabled(value):
    if value is not None:
        return False
    return True

# Отправка выбранного адреса на back
@dash.callback(
    Output('message_from_server', 'children'),
    Input('button_connection', 'n_clicks'),
    State('dropdown', 'value'),
    prevent_initial_call=True,
)
def send_address(bt1, value):
    if value is not None:
        post = requests.post('http://127.0.0.1:5001/post', json=value).json()
        # os.system('python3 output.py &')
        return f'Server response: {post[0]}'
    