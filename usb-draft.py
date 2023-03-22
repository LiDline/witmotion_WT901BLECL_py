from dash_extensions import WebSocket
from dash_extensions.enrich import html, Output, Input, State, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash
import re
import os
from dash import DiskcacheManager, CeleryManager
import requests
import json


# Для background
if 'REDIS_URL' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery
    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(celery_app)
else:
    # Diskcache for non-production apps when developing locally
    import diskcache
    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)


from func.func_dash.app_content import header_page
from func.func_dash.inputs import input_address
from func.func_dash.buttons import connection, start
from func.counter import Counter


# dash.register_page(__name__)
# ___________________________________________________________________________________________________

# Client-side function (for performance) that updates the graph.
with open('func/graph.js') as f:    # plot the data
    update_graph = f.read()
# ___________________________________________________________________________________________________

'''layout'''

layout = html.Div([
    # Storage
    dcc.Store(id='input-data'),
    dcc.Store(id='output-data'),

    # Header
    dbc.Row([
            dbc.Col([
                header_page(re.sub(r'\w+\.', '', __name__)),
            ])
            ]),

    # Input
    dbc.Row([
            dbc.Col([
                    input_address()
                    ], width={"size": 3}),
            WebSocket(id="ws", url="ws://127.0.0.1:5000/ws"),
    # Connection
            dbc.Col([
                    connection()
                    ]),
            dbc.Col([
                    html.Div(id='message')
                    ])
            ], className='other'),
    dbc.Row([
            html.Div(start())
            ], className='other'),
    dbc.Row([
            html.Div(id='graph_row')
            ], className='other'),
])

'''Callback'''

# Storage Input
@dash.callback(
    Output('input-data', 'data'),
    Input("ws", "message"),
    prevent_initial_call=True,
    # Не обязательно
    # background=True,
    # manager=background_callback_manager,
)
def text(e):
    if e['data'] == 'sensor is connected' or e['data'] == "sensor isn't connected":
        return e
    return dash.no_update 

# # Storage Output
# @dash.callback(
#     Output('ws', 'send', allow_duplicate=True),
#     Input("interval", "n_intervals"),
#     State('button_connection', 'n_clicks'),
#     prevent_initial_call=True,
# )
# def send(n, bt1):
#     button_counter = Counter()
#     return f'{button_counter.count}. button_start'

# Кнопки connection и start - связь с webSocket
@dash.callback(
    Output("ws", "send", allow_duplicate=True),
    Output("graph_row", "children"),
    Input('button_connection', 'n_clicks'),
    Input('button_start', 'n_clicks'),
    State('input', 'value'),
    prevent_initial_call=True,
    )
def send(bt1, bt2, values):
    button_id = dash.ctx.triggered_id

    # Отправляем адрес
    if button_id == 'button_connection':
        button_counter = Counter()
        return [f'{button_counter.count}. ' + values, dash.no_update]
    elif button_id == 'button_start':
        button_counter = Counter()
        
        graph = html.Div(dcc.Graph(id='graph'))
        return [f'{button_counter.count}. {button_id}', dbc.Col([graph])]


# Приём ответов от webSocket
@dash.callback(
    Output("message", "children"),
    [Input("input-data", 'data')],
    prevent_initial_call=True
    )
def message(e):
    res = requests.get('http://127.0.0.1:5000/available_ports')
    json_ = res.json()
    if e['data'] == 'sensor is connected' or e['data'] == "sensor isn't connected":
            return f"Response from websocket: {json_}"
    return dash.no_update


# Активация кнопки Start только при положительном ответе от webSocket
@dash.callback(
    Output('button_connection', 'disabled'),
    Output('button_start', 'disabled'),
    Output("button_stop", 'disabled'),
    State('button_connection', 'n_clicks'),
    Input('button_start', 'n_clicks'),
    Input('button_stop', 'n_clicks'),
    Input('input-data', 'data'),
    prevent_initial_call=True,
)
def disabled(bt1, bt2, bt3, e):
    button_id = dash.ctx.triggered_id
    
    if button_id == 'button_start':
        return [True, True, False]
    elif button_id == 'button_stop':
        return [dash.no_update, False, True]
    elif e['data'] == 'sensor is connected':
        return [dash.no_update, False, dash.no_update]
    

# Приём данных с webSocket для графика
dash.clientside_callback(update_graph,
                         Output("graph", "figure"),
                         Input("ws", "message"),
                         prevent_initial_call=True
                         )
