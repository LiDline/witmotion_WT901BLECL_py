from dash_extensions import WebSocket
from dash_extensions.enrich import html, Input, Output, State, dcc
import requests
import time
import os


from func.components.buttons import start
from func.check_running_output import is_running


def callback(dash):   
    
    # Client-side function (for performance) that updates the graph.
    with open('func/graph.js') as f:    # plot the data
        update_graph = f.read()
        
    
    # 1. Обновление поля Selected | активация Selected и Device connection
    @dash.callback(
        Output('dropdown', 'disabled', allow_duplicate=True),
        Output('dropdown', 'options'),
        Input('button_search', 'n_clicks'),
        prevent_initial_call=True,
    ) 
    def selected(bt1):
        try:    # Иначе ругается на requests (при нажатии на Stop прога идёт сюда)
            ports = requests.get('http://127.0.0.1:5000/available_ports').json()
            return [False, ports]
        except:
            return [True, dash.no_update]


    # 2. Отправка выбранного адреса на back
    @dash.callback(
        Output('message_from_post_server', 'children', allow_duplicate=True),
        Input('dropdown', 'value'),
        prevent_initial_call=True,
    )
    def activations(value):
        if value != None:
            post = requests.post(
                'http://127.0.0.1:5000/chosen_address_input', json=value).json()
            return [f'Server response: {post[0]}']
        return dash.no_update


    # 3. Активация кнопок Sensor Settings и Start
    @dash.callback(
        Output('button_sensor_settings', 'disabled'),
        Output('button_sensor_settings', 'outline'),
        Output('button_start', 'disabled'),
        Output('button_start', 'outline'),
        Input('dropdown', 'value'),
        prevent_initial_call=True,
    )
    def disabled(value):
        if value != None:
            return [False, False, False, False]
        return [True, True, True, True]
    
    
    # 4. Открытие кнопки Settings
    @dash.callback(
        Output("collapse_sensor_settings", "is_open"),
        Input("button_sensor_settings", "n_clicks"),
        Input('dropdown', 'value'),
        State("collapse_sensor_settings", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_collapse(n, value, is_open):
        button_id = dash.ctx.triggered_id
        
        if value == None:
            return False
        elif button_id == 'button_sensor_settings':
            if n:
                return not is_open
            return is_open
    
    
    # 5. Работа кнопок в Settings (кроме Magnetometer calibration)
    @dash.callback(
        Output('message_from_post_server', 'children', allow_duplicate=True),
        Input('accelerometer_calibration', 'n_clicks'),
        Input('6_DOF', 'n_clicks'),
        Input('9_DOF', 'n_clicks'),
        Input('rate', 'value'),
        prevent_initial_call=True,
        background=True,
        running=[
            (Output("accelerometer_calibration", "disabled"), True, False),
            (Output("magnetometer_calibration", "disabled"), True, False),
            (Output("button_start", "disabled"), True, False),
            (Output("button_sensor_settings", "disabled"), True, False),
            (Output("button_search", "disabled"), True, False),
            (Output("6_DOF", "disabled"), True, False),
            (Output("9_DOF", "disabled"), True, False),
            (Output("dropdown", "disabled"), True, False),
            (Output("rate", "disabled"), True, False),
        ],
    )
    def sensor_settings(btn_acc, btn_six, btn_nine, rate):
        button_id = dash.ctx.triggered_id
        
        if button_id == 'rate':
            post = requests.post(
                    'http://127.0.0.1:5000/sensor_settings', json=[rate]).json()
            return html.Div(post[0])

        post = requests.post(
                    'http://127.0.0.1:5000/sensor_settings', json=[button_id]).json()   

        return html.Div(post[0])
    
    
    # 6. Кнопка Magnetometer calibration
    @dash.callback(
        Output("modal", "is_open"),
        Output('message_from_post_server', 'children'),
        Input("magnetometer_calibration", "n_clicks"), 
        Input("button_close", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_modal(n1, n2):
        button_id = dash.ctx.triggered_id

        if button_id == 'magnetometer_calibration':
            post = requests.post(
                    'http://127.0.0.1:5000/sensor_settings', json=[button_id]).json()
            return [True, dash.no_update]
        post = requests.post(
                    'http://127.0.0.1:5000/magnetometer_calibration_end', json=['end']).json()
        return [False, html.Div(post[0])]
    
    # 7. Замена кнопки Start на Stop
    @dash.callback(
        Output('button_start', 'color'),
        Output('button_start', 'children'),
        Input('button_start', 'n_clicks'),
        State('button_start', 'color'),
        prevent_initial_call=True,
    )
    def change(bt, color):
        if color == 'primary':
            return ["danger", 'Save & Stop']
        return ['primary', 'Start']
    
    
    # 8. Start/Stop
    @dash.callback(
        Output("button_sensor_settings", "disabled", allow_duplicate=True),
        Output("button_search", "disabled", allow_duplicate=True),
        Output("collapse_sensor_settings", "is_open", allow_duplicate=True),
        Output("websocket_html", "children"),
        Output("graph_row", "children"),
        Output('message_from_post_server', 'children', allow_duplicate=True),
        Output('dropdown', 'value', allow_duplicate=True),
        Output('dropdown', 'disabled', allow_duplicate=True),
        State("button_start", 'color'),
        Input("button_start", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_collapse(color, bt1):                
         # Запуск считывания
        if color == 'primary':
            websocket = WebSocket(id="ws", url="ws://127.0.0.1:5000/ws")
            graph = html.Div(dcc.Graph(id='graph'))
            post = requests.post('http://127.0.0.1:5000/start_stop', json=True).json()
            return [
                True, # disabled button_sensor_settings
                True, # disabled button search
                False, # show sensor_settings_collapse
                websocket, # create websocket_html
                graph, # create graph_row
                post[0], # message from server
                dash.no_update, # dropdown usb value
                True # dropdown usb disabled
                ]
        elif color == 'danger':
            # Остановка считывания и выключение сервера считывания 
            try:    # Иначе ругается на requests
                post = requests.post(
                    'http://127.0.0.1:5000/start_stop', json=False).json()
            except:
                os.system('python3 output.py &')    # При остановке считывания я убиваю output.py
            return [True, False, False, html.Div(), html.Div(), 
                    'Server response: reading complete, data is saved in the project folder in "res.csv"!', 
                    None, False]

   
   # 9. Приём данных с webSocket для графика
    dash.clientside_callback(update_graph,
                         Output("graph", "figure"),
                         Input("ws", "message"),
                         prevent_initial_call=True
                         )  
    
    #===================================================================================
    
    
#  Callback главных кнопок в app.py
def buttons_main_callback(dash):
    pages = [page["relative_path"] for page in dash.page_registry.values()]
    
    @dash.callback(
        [Output(f'{page["relative_path"]}', 'disabled') for page in dash.page_registry.values()],
        Input('url', 'pathname'),
        prevent_initial_call=True,
        # background=True,
        # running=[
        #     (Output("button_search", "disabled"), True, False),
        # ],
    )
    def disabled(path):
        # Проверка запущен ли webserver (output.py)
        if is_running('output.py') == False:
            os.system('python3 output.py &')
            time.sleep(0.75)
            
        # Находим кнопку, id которой совпадает с page и по индексу в списке гасим
        command = [False for page in dash.page_registry.values()]
        index = pages.index(path)

        # Меняем её disable на False
        del command[index]
        command.insert(index, True)
        
        post = requests.post(
            'http://127.0.0.1:5000/sensor_selection', json=path).json() # Отправим usb/bluetooth

        return command