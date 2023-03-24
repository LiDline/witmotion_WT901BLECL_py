from dash_extensions import WebSocket
from dash_extensions.enrich import html, Input, Output, State, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash
import re
import os
import requests
import time


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
    Output('message_from_post_server', 'children', allow_duplicate=True),
    Output('button_sensor_settings', 'disabled', allow_duplicate=True),
    Input('button_connection', 'n_clicks'),
    State('dropdown', 'value'),
    prevent_initial_call=True,
)
def send_address(bt1, value):
    if value is not None:
        post = requests.post(
            'http://127.0.0.1:5001/chosen_address_input', json=value).json()
        return [f'Server response: {post[0]}', False]

# Открываем Settings
@dash.callback(
    Output("collapse_sensor_settings", "is_open", allow_duplicate=True),
    Input("button_sensor_settings", "n_clicks"),
    State("collapse_sensor_settings", "is_open"),
    prevent_initial_call=True,
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Общая работа кнопок
@dash.callback(
    Output("button_start", "disabled"),
    Output("button_stop", "disabled"),
    Output("button_sensor_settings", "disabled"),
    Output("collapse_sensor_settings", "is_open"),
    Output("websocket_html", "children"),
    Output("graph_row", "children"),
    Output('message_from_post_server', 'children', allow_duplicate=True),
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
            return [
                False, # disabled button_start
                dash.no_update, # disabled button_stop
                False, # disabled button_sensor_settings
                False, # show sensor_settings_collapse
                dash.no_update, # create websocket_html
                dash.no_update,  # create graph_row
                dash.no_update, # message from server
                ] 
        # Запуск считывания
        elif button_id == 'button_start':
            graph = html.Div(dcc.Graph(id='graph'))
            websocket = WebSocket(id="ws", url="ws://127.0.0.1:5000/ws")
            post = requests.post(
                'http://127.0.0.1:5001/start_stop', json=True).json()
            return [True, False, True, False, websocket, graph, post[0]]
        # Остановка считывания и выключение сервера считывания 
        elif button_id == 'button_stop':
            post = requests.post(
                'http://127.0.0.1:5001/start_stop', json=False).json()
            return [True, True, True, False, html.Div(), html.Div(), post[0]]
        
    # Перестраховка    
    post = requests.post(
                'http://127.0.0.1:5001/start_stop', json=False).json()
    return [True, True, True, False, html.Div(), html.Div(), dash.no_update] 


# Функционал Sensor settings
@dash.callback(
    Output('message_from_post_server', 'children'),
    Input('accelerometer_calibration', 'n_clicks'),
    Input('magnetometer_calibration', 'n_clicks'),
    Input('6_DOF', 'n_clicks'),
    Input('9_DOF', 'n_clicks'),
    Input('rate', 'value'),
    prevent_initial_call=True,
    background=True,
    running=[
        (Output("accelerometer_calibration", "disabled"), True, False),
        (Output("magnetometer_calibration", "disabled"), True, False),
        (Output("button_start", "disabled"), True, False),
        (Output("button_sensor_settings", "disabled"), True, False),
        (Output("button_connection", "disabled"), True, False),
        (Output("button_search", "disabled"), True, False),
        (Output("6_DOF", "disabled"), True, False),
        (Output("9_DOF", "disabled"), True, False),
        (Output("dropdown", "disabled"), True, False),
        (Output("rate", "disabled"), True, False),
    ],
)
def sensor_settings(bt_acc, btn_magn, btn_six, btn_nine, rate):
    button_id = dash.ctx.triggered_id
    if button_id == 'rate':
        post = requests.post(
                'http://127.0.0.1:5001/sensor_settings', json=[rate]).json()
        return html.Div(post[0])
        
    post = requests.post(
                'http://127.0.0.1:5001/sensor_settings', json=[button_id]).json()    
    return html.Div(post[0])

# Приём данных с webSocket для графика
dash.clientside_callback(update_graph,
                         Output("graph", "figure"),
                         Input("ws", "message"),
                         prevent_initial_call=True
                         ) 