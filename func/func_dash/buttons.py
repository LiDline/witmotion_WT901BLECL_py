import dash_bootstrap_components as dbc


# Кнопка подключение
def start():
    start = dbc.Button("Start", color="primary", id='button_start', n_clicks=0, size="lg",)
    return start