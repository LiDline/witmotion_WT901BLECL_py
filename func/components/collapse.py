import dash_bootstrap_components as dbc
from func.components.buttons import acc_cal, algorithm_transition
from func.components.drop_menu import rate
from func.components.modal import modal


def collapse_settings():
    return  dbc.Collapse(
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
        )
