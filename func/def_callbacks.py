import time
import os
import requests
import dash
import subprocess
from dash_extensions.enrich import html


from func.components.collapse import collapse
from func.components.buttons import start


# 1. Обновление поля Selected | активация Selected и Device connection 
def control_settings():
    # Проверка запущен ли webserver (output.py)

        # os.system('python3 output.py &')
        # time.sleep(1)
        
    try:    # Иначе ругается на requests (при нажатии на Stop прога идёт сюда)
        ports = requests.get('http://127.0.0.1:5000/available_ports').json()
        return [False, ports]
    except:
        return [True, dash.no_update]
    

# 2. Активация|деактивация кнопки Device connection
def control_device_connection(value):
    if value is not None:
        return False
    return True    


# 3. Отправка выбранного адреса на back
def send_address(value):
    # if value is not None:
        post = requests.post(
            'http://127.0.0.1:5000/chosen_address_input', json=value).json()
        return [f'Server response: {post[0]}']
    
    
# 4. Активация кнопок Sensor settings, Start и Stop
def activations_settings_start_stop(button_id, value):
    if value != None and button_id == 'button_connection':
        return [collapse(), start()]
    return [html.Div(), html.Div()]


# 5. Открытие кнопки Settings
def settings_collapse(n, is_open):
    if n:
        return not is_open
    return is_open