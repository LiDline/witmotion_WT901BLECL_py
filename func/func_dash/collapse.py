import dash_bootstrap_components as dbc
from dash_extensions.enrich import html


def collapse():
    res = [
        dbc.Button(
            "Sensor settings",
            id="Settings",
            className="mb-3",
            color="primary",
            n_clicks=0,),
        dbc.Collapse(
            dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
            id="collapse",
            is_open=False,
        ),
    ]
    return html.Div(res)
