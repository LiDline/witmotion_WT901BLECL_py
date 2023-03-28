import dash_bootstrap_components as dbc


# Кнопка подключение
def connection():
    button_group = dbc.ButtonGroup([
        dbc.Button("Search devices", outline=True, color="primary",
                   id='button_search', n_clicks=0, disabled=False),
        dbc.Button("Device connection", outline=True, color="primary",
                   id='button_connection', n_clicks=0, disabled=True)
    ])
    return button_group


# Кнопка калибровки акс
def acc_cal():
    return dbc.Button(
            "Accelerometer calibration",
            id="accelerometer_calibration",
            className="mb-3",
            color="primary",
            n_clicks=0, 
            outline=True,
            disabled=False)


# Количество степеней
def algorithm_transition():
    return  dbc.ButtonGroup([
        dbc.Button("6-DOF", outline=True, color="primary",
                   id='6_DOF', n_clicks=0, disabled=False),
        dbc.Button("9-DOF", outline=True, color="danger",
                   id='9_DOF', n_clicks=0, disabled=False),
    ])  


# Кнопка старта
def start():
    return dbc.ButtonGroup([
        dbc.Button("Start", outline=True, color="primary",
                   id='button_start', n_clicks=0, disabled=False),
        dbc.Button("Stop", outline=True, color="danger",
                   id='button_stop', n_clicks=0, disabled=False),
    ], size="lg", )
     

# Sensor settings
def button_sensor_settings():
    return dbc.Button(
            "Sensor settings",
            id="button_sensor_settings",
            className="mb-3",
            color="primary",
            n_clicks=0, 
            disabled=False)