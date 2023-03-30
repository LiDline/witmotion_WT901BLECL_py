from dash_extensions import WebSocket
from dash_extensions.enrich import html, Input, Output, State
import requests
import time
import os


from func.components.collapse import collapse_settings
from func.components.buttons import start
from func.check_running_output import is_running


def callback(dash):   
    # 1. Обновление поля Selected | активация Selected и Device connection
    @dash.callback(
        Output('dropdown', 'disabled', allow_duplicate=True),
        Output('dropdown', 'options'),
        Input('button_search', 'n_clicks'),
        State('url', 'pathname'),
        prevent_initial_call=True,
        background=True,
    ) 
    def selected(bt1, path):
        # Проверка запущен ли webserver (output.py)
        if is_running('output.py') == False:
            os.system('python3 output.py &')
            time.sleep(1)

        try:    # Иначе ругается на requests (при нажатии на Stop прога идёт сюда)
            post = requests.post(
                'http://127.0.0.1:5000/sensor_selection', json=path).json() # Отправим usb/bluetooth
            ports = requests.get('http://127.0.0.1:5000/available_ports').json()
            return [False, ports]
        except:
            return [True, dash.no_update]



    '''Убрать эту кнопку нахуй и заменить на сеттинг
    И чтобы кнопка цветом заливалась'''
    # 2. Активация|деактивация кнопки Device connection
    @dash.callback(
        Output('button_connection', 'disabled'),
        Input('dropdown', 'value'),
        prevent_initial_call=True,
    )
    def disabled(value):
        if value is not None:
            return False
        return True  


    # 3. Отправка выбранного адреса на back
    @dash.callback(
        Output('message_from_post_server', 'children', allow_duplicate=True),
        Input('button_connection', 'n_clicks'),
        State('dropdown', 'value'),
        prevent_initial_call=True,
    )
    def activations(bt1, value):
        # if value is not None:
        post = requests.post(
            'http://127.0.0.1:5000/chosen_address_input', json=value).json()
        return [f'Server response: {post[0]}']


    # # 4. Активация кнопок Sensor settings, Start и Stop
    # @dash.callback(
    #     Output('html_sensor_settings', 'children'),
    #     Output('html_buttons_start_and_stop', 'children'),
    #     Input('button_connection', 'n_clicks'),
    #     Input('dropdown', 'value'),
    #     prevent_initial_call=True,
    # )
    # def disabled(bt1, value):
    #     button_id = dash.ctx.triggered_id
    #     if value != None and button_id == 'button_connection':
    #         return [collapse_settings(), start()]
    #     return [html.Div(), html.Div()]
    
    
    # # 5. Открытие кнопки Settings
    # @dash.callback(
    #     Output("collapse_sensor_settings", "is_open", allow_duplicate=True),
    #     Input("button_sensor_settings", "n_clicks"),
    #     State("collapse_sensor_settings", "is_open"),
    #     prevent_initial_call=True,
    # )
    # def toggle_collapse(n, is_open):
    #     if n:
    #         return not is_open
    #     return is_open
    
    
    # # 6. Работа кнопок в Settings
    # @dash.callback(
    #     Output('message_from_post_server', 'children', allow_duplicate=True),
    #     Input('accelerometer_calibration', 'n_clicks'),
    #     Input('6_DOF', 'n_clicks'),
    #     Input('9_DOF', 'n_clicks'),
    #     Input('rate', 'value'),
    #     prevent_initial_call=True,
    #     background=True,
    #     running=[
    #         (Output("accelerometer_calibration", "disabled"), True, False),
    #         (Output("magnetometer_calibration", "disabled"), True, False),
    #         (Output("button_start", "disabled"), True, False),
    #         (Output("button_stop", "disabled"), True, False),
    #         (Output("button_sensor_settings", "disabled"), True, False),
    #         (Output("button_connection", "disabled"), True, False),
    #         (Output("button_search", "disabled"), True, False),
    #         (Output("6_DOF", "disabled"), True, False),
    #         (Output("9_DOF", "disabled"), True, False),
    #         (Output("dropdown", "disabled"), True, False),
    #         (Output("rate", "disabled"), True, False),
    #     ],
    # )
    # def sensor_settings(btn_acc, btn_six, btn_nine, rate):
    #     button_id = dash.ctx.triggered_id
    #     print(button_id)
    #     if button_id == 'rate':
    #         post = requests.post(
    #                 'http://127.0.0.1:5000/sensor_settings', json=[rate]).json()
    #         return html.Div(post[0])

    #     post = requests.post(
    #                 'http://127.0.0.1:5000/sensor_settings', json=[button_id]).json()   

    #     return html.Div(post[0])

#=================================================================================================
#  Callback главных кнопок в app.py
def buttons_main_callback(dash):
    pages = [page["relative_path"] for page in dash.page_registry.values()]
    
    @dash.callback(
        [Output(f'{page["relative_path"]}', 'disabled') for page in dash.page_registry.values()],
        Input('url', 'pathname'),
        prevent_initial_call=True,
    )
    def disabled(path):
        # Находим кнопку, id которой совпадает с page и по индексу в списке гасим
        command = [False for page in dash.page_registry.values()]
        index = pages.index(path)

        # Меняем её disable на False
        del command[index]
        command.insert(index, True)
        return command