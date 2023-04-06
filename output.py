import json
from quart import websocket, Quart, request
import serial
import time
from numpy import concatenate
import serial
import sys
from bleak import BleakClient, BleakScanner
import nest_asyncio
from func.for_bluetooth import Bluetooth


from func.general_operations import di_commands
from func.for_usb import usb_calibrate_gyr_and_acc, usb_algorithm_transition, usb_return_rate
from func.for_usb import serial_ports
from func.general_operations import create_table, decoded_data


app = Quart(__name__)

address = None
command = None
sensor = None
rate = 10  # default


# Usb/Bluetooth
@app.post("/sensor_selection")
async def sensor_selection():
    global sensor
    sensor = await request.get_json()
    return [sensor]


# Для отправки доступных адресов
@app.get("/available_ports")
async def ports():
    try:
        await client.disconnect()   # На всякий случай отрубим то, что подключили 
    except:
        pass    
    print(sensor)
    if sensor == '/usb':
        return serial_ports()
    elif sensor == '/bluetooth':
        devices = await BleakScanner.discover(timeout=1)
        return [dev.address for dev in devices if 'WT901' in dev.name]


# Для приёма выбранного адреса
@app.post("/chosen_address_input")
async def chosen_address_output():
    global address, socket, client  # По другому не придумал...
    
    try:
        await client.disconnect()
    except:
        pass
    
    address = await request.get_json()

    if sensor == '/usb':
        socket = serial.Serial(address, 115200, timeout=10)
        if socket.open:
            return [f'input "{address}" is available.']

    elif sensor == '/bluetooth':
        client = BleakClient(address)
        await client.connect()
        return [f'input "{address}" is available.']

    return [f"input '{address}' isn't available. Please, push search button!"]


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


# Каллибровка
@app.post("/sensor_settings")
async def sensor_settings():
    settings = await request.get_json()

    if settings[0] == 'accelerometer_calibration':
        usb_calibrate_gyr_and_acc(socket)
    elif settings[0] == '6_DOF' or settings[0] == '9_DOF':
        usb_algorithm_transition(socket, settings[0])
    elif settings[0] in [0.2, 0.5, 1, 2, 5, 10, 20, 50]:
        global rate
        rate = settings[0]
        usb_return_rate(socket, settings[0])
    elif settings[0] == 'magnetometer_calibration':
        socket.write(di_commands('magnetometer_calibration'))
    return [f'Server response: command {settings[0]} is complete!']


# Завершение магнитной калибровки
@app.post("/magnetometer_calibration_end")
async def magnetometer_calibration_end():
    end_step = await request.get_json()
    socket.write(di_commands('exit_calibration_mode'))
    return [f'Server response: command magnetometer_calibration is end!']


df = create_table()


# Создаём вебсокеты
@app.websocket("/ws")
async def data():
    t_start = time.perf_counter()

    if sensor == '/usb':
        socket = serial.Serial(address, 115200, timeout=rate)
        while command:
            data = socket.read(20)
            a, w, A = decoded_data(data)
            df.loc[len(df.index)] = concatenate(
                [[round(time.perf_counter() - t_start, 2)], a, w, A])
            output = json.dumps([
                (df[df.columns[i]].tail(50)).to_list() for i in range(len(df.axes[1]))
            ])
            await websocket.send(output)
# =======================================================================================
    elif sensor == '/bluetooth':
        nest_asyncio.apply()
        bluetooth = Bluetooth(rate)

        t_start = time.perf_counter()

        while command:
            a, w, A = await bluetooth.bluetooth_run_async(client)

            df.loc[len(df.index)] = concatenate(
                [[round(time.perf_counter() - t_start, 2)], a, w, A])

            output = json.dumps([
                (df[df.columns[i]].tail(50)).to_list() for i in range(len(df.axes[1]))
            ])

            await websocket.send(output)
    
    df.to_csv('res.csv')
    try: 
        await client.stop_notify("0000ffe4-0000-1000-8000-00805f9a34fb")
        await client.disconnect()   # Программа крашится с ошибкой, да и хер с ней, я так и задумывал
    except:
        sys.exit()


if __name__ == "__main__":
    app.run(port=5000)
