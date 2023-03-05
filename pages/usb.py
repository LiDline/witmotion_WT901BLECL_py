from dash_extensions import WebSocket
from dash_extensions.enrich import html, Output, Input, State, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash
import re


from func.general_operations import create_table, decoded_data
from func.func_dash.app_content import header_page
from func.func_dash.inputs import input_adress
from func.func_dash.buttons import start


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
                ], width={"size": 3})
            ], className='other'),
    
    # Кнопка старт
    dbc.Row([
        dbc.Col([
            start()
            ])
        ], className='other'),
    # График
    html.Div(id='plot')
    ])


# Кнопка старт
@dash.callback(
    [Output('plot', 'children')], 
    [Input('button_start', 'n_clicks')],
    State('input', 'value'),
    prevent_initial_call=True)
def start_button(n_clicks, values):
    res = dbc.Row([
        dbc.Col([
            dcc.Graph(id="graph"), WebSocket(id="ws", url="ws://127.0.0.1:5000/WT901"),
            ]),
        ])
    return [res]


dash.clientside_callback(update_graph, 
                        Output("graph", "figure"), 
                        Input("ws", "message"),
                        )