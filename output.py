import json
from quart import websocket, Quart
import serial
import time
from numpy import concatenate
import requests
import sys


from func.general_operations import create_table, decoded_data


app = Quart(__name__)


df = create_table()
t_start = time.perf_counter()

@app.websocket("/ws")
async def data():
    address = requests.get('http://127.0.0.1:5001/chosen_address_output').json()[0]
    command = requests.get('http://127.0.0.1:5001/executed_order').json()[0]
    socket = serial.Serial(address, 115200, timeout=10)
    print(command)
    while command:
        data = socket.read(20)
        a, w, A = decoded_data(data)
        df.loc[len(df.index)] = concatenate([[round(time.perf_counter() - t_start, 2)], a, w, A])
        output = json.dumps([
            (df[df.columns[i]].tail(50)).to_list() for i in range(len(df.axes[1]))
            ])
        await websocket.send(output)
        
        command = requests.get('http://127.0.0.1:5001/executed_order').json()[0]
        time.sleep(0.1)
    sys.exit()
    

if __name__ == "__main__":
    app.run(port=5000,
            )