from dash_extensions import WebSocket
from dash_extensions.enrich import html, Input, Output, State, dcc
import dash_bootstrap_components as dbc
import dash
import re
import os
import requests
import time


from func.components.app_content import header_page
from func.components.drop_menu import drop_menu
from func.components.collapse import collapse
from func.components.buttons import connection, start


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
        # Sensor settings
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
    Output('dropdown', 'disabled', allow_duplicate=True),
    Output('dropdown', 'options'),
    Input('button_search', 'n_clicks'),
    prevent_initial_call=True,
    background=True,
)
def disabled(bt1):
    os.system('python3 output.py &')
    time.sleep(1)
    try:    # Иначе ругается на requests (при нажатии на Stop прога идёт сюда)
        ports = requests.get('http://127.0.0.1:5000/available_ports').json()
        return [False, ports]
    except:
        return [True, dash.no_update]

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
            'http://127.0.0.1:5000/chosen_address_input', json=value).json()
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
    Output('dropdown', 'value'),
    Output('dropdown', 'disabled', allow_duplicate=True),
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
            # os.system('python3 output.py &')
            return [
                False, # disabled button_start
                dash.no_update, # disabled button_stop
                False, # disabled button_sensor_settings
                False, # show sensor_settings_collapse
                dash.no_update, # create websocket_html
                dash.no_update,  # create graph_row
                dash.no_update, # message from server
                dash.no_update, # dropdown usb value
                dash.no_update, # dropdown usb disabled
                ] 
        # Запуск считывания
        elif button_id == 'button_start':
            websocket = WebSocket(id="ws", url="ws://127.0.0.1:5000/ws")
            graph = html.Div(dcc.Graph(id='graph'))
            post = requests.post(
                'http://127.0.0.1:5000/start_stop', json=True).json()
            return [True, False, True, False, websocket, graph, post[0], dash.no_update, True]
        # Остановка считывания и выключение сервера считывания 
        elif button_id == 'button_stop':
            try:    # Иначе ругается на requests
                post = requests.post(
                    'http://127.0.0.1:5000/start_stop', json=False).json()
            except:
                pass
            return [True, True, True, False, html.Div(), html.Div(), 
                    'Server response: reading complete, data is saved in the project folder in "res.csv"!', 
                    None, True]
        
    # Перестраховка    
    post = requests.post(
                'http://127.0.0.1:5000/start_stop', json=False).json()
    return [True, True, True, False, html.Div(), html.Div(), dash.no_update, dash.no_update, dash.no_update] 


# Функционал Sensor settings
@dash.callback(
    Output('message_from_post_server', 'children', allow_duplicate=True),
    Input('accelerometer_calibration', 'n_clicks'),
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
def sensor_settings(btn_acc, btn_six, btn_nine, rate):
    button_id = dash.ctx.triggered_id

    if button_id == 'rate':
        post = requests.post(
                'http://127.0.0.1:5000/sensor_settings', json=[rate]).json()
        return html.Div(post[0])
        
    post = requests.post(
                'http://127.0.0.1:5000/sensor_settings', json=[button_id]).json()   
     
    return html.Div(post[0])


# Кнопка Magnetometer calibration
@dash.callback(
    Output("modal", "is_open"),
    Output('message_from_post_server', 'children'),
    Input("magnetometer_calibration", "n_clicks"), 
    Input("button_close", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_modal(n1, n2):
    button_id = dash.ctx.triggered_id
    
    if button_id == 'magnetometer_calibration':
        post = requests.post(
                'http://127.0.0.1:5000/sensor_settings', json=[button_id]).json()
        return [True, dash.no_update]
    post = requests.post(
                'http://127.0.0.1:5000/sensor_settings', json=['magnetometer_calibration']).json()
    return [False, html.Div(post[0])]


# Приём данных с webSocket для графика
dash.clientside_callback(update_graph,
                         Output("graph", "figure"),
                         Input("ws", "message"),
                         prevent_initial_call=True
                         ) 