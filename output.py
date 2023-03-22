import json
from quart import websocket, Quart
import serial
import time
from numpy import concatenate
import requests


from func.general_operations import create_table, decoded_data
from func.serial_ports import serial_ports

app = Quart(__name__)

df = create_table()

t_start = time.perf_counter()

@app.websocket("/ws")
async def data():
    while True:
        address = requests.get('http://127.0.0.1:5001/chosen_address_output').json()[0]
        if address == None:
            time.sleep(1)
        try:
            socket = serial.Serial(address, 115200, timeout=10)
            
            data = socket.read(20)
            a, w, A = decoded_data(data)
            df.loc[len(df.index)] = concatenate([[round(time.perf_counter() - t_start, 2)], a, w, A])
            output = json.dumps([
                (df[df.columns[i]].tail(50)).to_list() for i in range(len(df.axes[1]))
                ])
            await websocket.send(output)
            
            time.sleep(0.1)


        except:
            continue

if __name__ == "__main__":
    app.run(port=5000)