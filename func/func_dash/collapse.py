import dash_bootstrap_components as dbc
from dash_extensions.enrich import html
from func.func_dash.buttons import button_sensor_settings, acc_cal, algorithm_transition
from func.func_dash.drop_menu import rate
from func.func_dash.modal import modal


def collapse():
    res = [
        button_sensor_settings(),
        dbc.Collapse(
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        acc_cal()
                    ]),
                    dbc.Col([
                        algorithm_transition()
                    ]), 
                ]),
                dbc.Row([
                    dbc.Col([
                        modal()
                        
                    ]),
                    dbc.Col([
                        rate()
                    ]), 
                ])
            ]),
            id="collapse_sensor_settings",
            is_open=False,
        ),
    ]
    return html.Div(res)
