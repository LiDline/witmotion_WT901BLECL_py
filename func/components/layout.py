import re
import dash_bootstrap_components as dbc
from dash_extensions.enrich import html
from func.components.collapse import collapse


from func.components.app_content import header_page
from func.components.drop_menu import drop_menu
from func.components.buttons import connection


# Layout 
def layout(name):
    return html.Div([
    # Websocket
    html.Div(id='websocket_html'),
    # Header
    dbc.Row([
            dbc.Col([
                header_page(re.sub(r'\w+\.', '', name)),
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
        ], width={"size": 4}),
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