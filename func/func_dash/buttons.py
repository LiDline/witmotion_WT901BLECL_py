import dash_bootstrap_components as dbc


# Кнопка подключение
def connection():
    connection = dbc.Button("Сonnection", outline=True, color="primary", id='button_connection', n_clicks=0)
    return connection


# Кнопка старта
def start():
    button_group = dbc.ButtonGroup([
        dbc.Button("Start", outline=True, color="primary", id='button_start', n_clicks=0),
        dbc.Button("Stop", outline=True, color="danger", id='button_stop', n_clicks=0),
    ], size="lg", )
    return button_group