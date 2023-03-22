import dash_bootstrap_components as dbc


# Кнопка подключение
def connection():
    button_group = dbc.ButtonGroup([
        dbc.Button("Search", outline=True, color="primary",
                   id='button_search', n_clicks=0, disabled=False),
        dbc.Button("Сonnection", outline=True, color="primary",
                   id='button_connection', n_clicks=0, disabled=True)
    ])
    return button_group


# Кнопка старта
def start():
    button_group = dbc.ButtonGroup([
        dbc.Button("Start", outline=True, color="primary",
                   id='button_start', n_clicks=0, disabled=True),
        dbc.Button("Stop", outline=True, color="danger",
                   id='button_stop', n_clicks=0, disabled=True),
    ], size="lg", )
    return button_group
