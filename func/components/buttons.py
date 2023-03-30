import dash_bootstrap_components as dbc


# Кнопка поиска
def button_search():
    return  dbc.Button("Search devices", outline=True, color="primary",
                   id='button_search', n_clicks=0, disabled=False)


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
    return dbc.Button("Start", outline=False, color="primary", size="lg",
                   id='button_start', n_clicks=0, disabled=False)
     

# Sensor settings
def button_sensor_settings():
    return dbc.Button(
            "Sensor settings",
            id="button_sensor_settings",
            color="success",
            n_clicks=0, 
            outline=True,
            disabled=True)