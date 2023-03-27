import json
from quart import websocket, Quart, request
import serial
import time
from numpy import concatenate
import sys
import serial


from func.general_operations import di_commands
from func.for_usb import usb_calibrate_gyr_and_acc, usb_algorithm_transition, usb_return_rate
from func.serial_ports import serial_ports
from func.general_operations import create_table, decoded_data


app = Quart(__name__)
address = None
command = None


# Для отправки доступных адресов
@app.get("/available_ports")
async def ports():
    available_ports = serial_ports()
    return available_ports


# Для приёма выбранного адреса
@app.post("/chosen_address_input")
async def chosen_address_output():
    global address, socket  # По другому не придумал...

    address = await request.get_json()
    socket = serial.Serial(address, 115200, timeout=10)
    if socket.open:
        return [f'input "{address}" is available.']
    return [f"input '{address}' isn't available."]

@app.get("/chosen_address_output")
async def chosen_address_input():
    return [address]
    
    
 # Start/Stop
@app.post("/start_stop")
async def start_stop(): 
    global command
    command = await request.get_json()
    if command:
        return ['Server response: data collection started!']
    return ['Server response: reading complete, data is saved in the project folder in "res.csv"!']

@app.get("/executed_order")
async def executed_order():
    return [command]


# Settings
@app.post("/sensor_settings")
async def sensor_settings():
    settings = await request.get_json()

    if settings[0] == 'accelerometer_calibration':
        usb_calibrate_gyr_and_acc(socket)
    elif settings[0] == '6_DOF' or settings[0] == '9_DOF':
        usb_algorithm_transition(socket, settings[0])    
    elif settings[0] in [0.2, 0.5, 1, 2, 5, 10 , 20, 50]:
        usb_return_rate(socket, settings[0])   
        
        """Не сделано"""
        
    elif settings[0] == 'magnetometer_calibration':
        socket.write(di_commands('magnetometer_calibration'))
        print(1)
        next_step = await request.get_json()
    socket.write(di_commands('exit_calibration_mode'))
    print(2)
    
    return [f'Server response: command {settings[0]} is complete!']


df = create_table()


# Создаём вебсокеты
@app.websocket("/ws")
async def data():
    # address = requests.get('http://127.0.0.1:5000/chosen_address_output').json()[0]
    # command = requests.get('http://127.0.0.1:5000/executed_order').json()[0]
    socket = serial.Serial(address, 115200, timeout=10)
    t_start = time.perf_counter()
    
    while command:
        data = socket.read(20)
        a, w, A = decoded_data(data)
        df.loc[len(df.index)] = concatenate([[round(time.perf_counter() - t_start, 2)], a, w, A])
        output = json.dumps([
            (df[df.columns[i]].tail(50)).to_list() for i in range(len(df.axes[1]))
            ])
        await websocket.send(output)
        print(command)
        # command = requests.get('http://127.0.0.1:5000/executed_order').json()[0]
    df.to_csv('res.csv')    
    sys.exit()
    

if __name__ == "__main__":
    app.run(port=5000,
            )