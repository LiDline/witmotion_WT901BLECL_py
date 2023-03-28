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


from func.def_callbacks import control_settings, control_device_connection, send_address, activations_settings_start_stop


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
            html.Div(id='html_sensor_settings')
        ], width={"size": 5}),
    ], className='other'),
        
    dbc.Row([
        dbc.Col([
            html.Div(id='html_buttons_start_and_stop')
            ]),
    ], className='other'),
    # Graph
    dbc.Row([
            html.Div(id='graph_row')
            ], className='other'),
])
# ___________________________________________________________________________________________________

'''Callback'''

# 1. Обновление поля Selected | активация Selected и Device connection
@dash.callback(
    Output('dropdown', 'disabled', allow_duplicate=True),
    Output('dropdown', 'options'),
    Input('button_search', 'n_clicks'),
    prevent_initial_call=True,
    background=True,
) 
def selected(bt1):
    return control_settings()


# 2. Активация|деактивация кнопки Device connection
@dash.callback(
    Output('button_connection', 'disabled'),
    Input('dropdown', 'value'),
    prevent_initial_call=True,
)
def disabled(value):
    return control_device_connection(value)


# 3. Отправка выбранного адреса на back и активация Settings, Start, Stop
@dash.callback(
    # Output('html_sensor_settings', 'children'),
    # Output('html_buttons_start_and_stop', 'children'),
    Output('message_from_post_server', 'children', allow_duplicate=True),
    Input('button_connection', 'n_clicks'),
    State('dropdown', 'value'),
    prevent_initial_call=True,
)
def activations(bt1, value):
    return send_address(value)


# 4. Активация кнопок Sensor settings, Start и Stop
@dash.callback(
    Output('html_sensor_settings', 'children'),
    Output('html_buttons_start_and_stop', 'children'),
    Input('button_connection', 'n_clicks'),
    Input('dropdown', 'value'),
    prevent_initial_call=True,
)
def disabled(bt1, value):
    button_id = dash.ctx.triggered_id
    return activations_settings_start_stop(button_id, value)
    