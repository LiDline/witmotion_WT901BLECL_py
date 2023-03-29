from dash_extensions import WebSocket
from dash_extensions.enrich import html, Input, Output, State


from func.def_callbacks import control_settings, control_device_connection, send_address, activations_settings_start_stop, settings_collapse


def callback(dash):   
    # 1. Обновление поля Selected | активация Selected и Device connection
    @dash.callback(
        Output('dropdown', 'disabled', allow_duplicate=True),
        Output('dropdown', 'options'),
        Input('button_search', 'n_clicks'),
        prevent_initial_call=True,
        background=True,
    ) 
    def selected(bt1):
        return control_settings()


    # 2. Активация|деактивация кнопки Device connection
    @dash.callback(
        Output('button_connection', 'disabled'),
        Input('dropdown', 'value'),
        prevent_initial_call=True,
    )
    def disabled(value):
        return control_device_connection(value)


    # 3. Отправка выбранного адреса на back
    @dash.callback(
        Output('message_from_post_server', 'children', allow_duplicate=True),
        Input('button_connection', 'n_clicks'),
        State('dropdown', 'value'),
        prevent_initial_call=True,
    )
    def activations(bt1, value):
        return send_address(value)


    # 4. Активация кнопок Sensor settings, Start и Stop
    @dash.callback(
        Output('html_sensor_settings', 'children'),
        Output('html_buttons_start_and_stop', 'children'),
        Input('button_connection', 'n_clicks'),
        Input('dropdown', 'value'),
        prevent_initial_call=True,
    )
    def disabled(bt1, value):
        button_id = dash.ctx.triggered_id
        return activations_settings_start_stop(button_id, value)
    
    # 5. Открытие кнопки Settings
    @dash.callback(
        Output("collapse_sensor_settings", "is_open", allow_duplicate=True),
        Input("button_sensor_settings", "n_clicks"),
        State("collapse_sensor_settings", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_collapse(n, is_open):
        return settings_collapse(n, is_open)
    
    

#  callback главных кнопок
def buttons_main_callback(dash):
    pages = [page["relative_path"] for page in dash.page_registry.values()]
    
    @dash.callback(
        [Output(f'{page["relative_path"]}', 'disabled') for page in dash.page_registry.values()],
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def disabled(path):
        # Находим кнопку, id которой совпадает с page и по индексу в списке гасим
        url = path
        command = [False for page in dash.page_registry.values()]
        index = pages.index(url)

        # Меняем её disable на False
        del command[index]
        command.insert(index, True)
        return command