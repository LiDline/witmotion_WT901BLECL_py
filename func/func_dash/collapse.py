import dash_bootstrap_components as dbc
from dash_extensions.enrich import html
from func.func_dash.buttons import settings, acc_cal, magn_cal, algorithm_transition
from func.func_dash.drop_menu import rate


def collapse():
    res = [
        settings(),
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
                        magn_cal()
                        
                    ]),
                    dbc.Col([
                        rate()
                    ]), 
                ])
            ]),
            id="collapse",
            is_open=False,
        ),
    ]
    return html.Div(res)
