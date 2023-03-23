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
from func.func_dash.collapse import collapse
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
    html.Div(id='websocket_html'),

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
            html.Div(id='message_from_post_server')
        ])
    ], className='other'),
    dbc.Row([
        dbc.Col([
            collapse()
        ], width={"size": 5}),
    ], className='other'),
    dbc.Row([
        dbc.Col([
            start()
            ]),
    ], className='other'),
    # Graph
    dbc.Row([
            html.Div(id='graph_row')
            ], className='other'),
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

# Отправка выбранного адреса на back и активация Settings
@dash.callback(
    Output('message_from_post_server', 'children'),
    Output('Settings', 'disabled'),
    Input('button_connection', 'n_clicks'),
    State('dropdown', 'value'),
    prevent_initial_call=True,
)
def send_address(bt1, value):
    if value is not None:
        post = requests.post(
            'http://127.0.0.1:5001/chosen_address_input', json=value).json()
        # os.system('python3 output.py &')
        return [f'Server response: {post[0]}', False]

# Открываем Settings
@dash.callback(
    Output("collapse", "is_open"),
    Input("Settings", "n_clicks"),
    State("collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Активация кнопки Start/Stop
@dash.callback(
    Output("button_start", "disabled"),
    Output("button_stop", "disabled"),
    Output("websocket_html", "children"),
    Output("graph_row", "children"),
    Input("button_start", "n_clicks"),
    Input("button_stop", "n_clicks"),
    Input('button_connection', "n_clicks"),
    Input('dropdown', 'value'),
    prevent_initial_call=True,
)
def toggle_collapse(bt1, bt2, bt3, value):
    button_id = dash.ctx.triggered_id

    if value != None:
        # Старт сервера считывания; активация кнопки Start
        if button_id == 'button_connection':
            os.system('python3 output.py &')
            return [False, dash.no_update, dash.no_update, dash.no_update]
        # Запуск считывания
        elif button_id == 'button_start':
            graph = html.Div(dcc.Graph(id='graph'))
            websocket = WebSocket(id="ws", url="ws://127.0.0.1:5000/ws")
            post = requests.post(
                'http://127.0.0.1:5001/start_stop', json=True).json()
            return [True, False, websocket, graph]
        # Остановка считывания и выключение сервера считывания 
        elif button_id == 'button_stop':
            post = requests.post(
                'http://127.0.0.1:5001/start_stop', json=False).json()
            return [True, True, html.Div(), html.Div()]
        
    # Перестраховка    
    post = requests.post(
                'http://127.0.0.1:5001/start_stop', json=False).json()
    return [True, True, html.Div(), html.Div()] 


# Приём данных с webSocket для графика
dash.clientside_callback(update_graph,
                         Output("graph", "figure"),
                         Input("ws", "message"),
                         prevent_initial_call=True
                         ) 