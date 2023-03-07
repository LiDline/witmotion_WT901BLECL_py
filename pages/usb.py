from dash_extensions import WebSocket
from dash_extensions.enrich import html, Output, Input, State, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash
import re


from func.general_operations import create_table, decoded_data
from func.func_dash.app_content import header_page
from func.func_dash.inputs import input_adress
from func.func_dash.buttons import connection, start


dash.register_page(__name__)
#___________________________________________________________________________________________________

# Client-side function (for performance) that updates the graph.
with open('func/graph.js') as f:    # plot the data
    update_graph = f.read()
#___________________________________________________________________________________________________

'''layout'''

layout = html.Div([
    # Storage
    dcc.Store(id='input-data'),
    
    # Header
    dbc.Row([
            dbc.Col([
                header_page(re.sub(r'\w+\.', '', __name__)),
                ])
            ]),
    
    # Input
    dbc.Row([
            dbc.Col([
                    input_adress()
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
            ], className='other')
    ])

'''Callback'''

# Кнопки
@dash.callback(
    Output("ws", "send"), 
    Input('button_connection', 'n_clicks'),
    Input('button_start', 'n_clicks'),
    State('input', 'value'),
    prevent_initial_call=True,
    )
def send(bt1, bt2, values):
    button_id = dash.ctx.triggered_id
    return values

# Приём состояния подключения
@dash.callback(
    Output("message", "children"),
    [Input("ws", 'message')],
    prevent_initial_call=True
    )
def message(e):
        return f"Response from websocket: {e['data']}"


dash.clientside_callback(update_graph, 
                        Output("graph", "figure"), 
                        Input("ws", "message"),
                        prevent_initial_call=True
                        )