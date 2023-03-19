import json
from quart import websocket, Quart
import serial
import time
from numpy import concatenate


from func.general_operations import create_table, decoded_data


app = Quart(__name__)

df = create_table()
t_start = time.perf_counter()

@app.websocket("/ws")
async def random_data():
    await websocket.accept()
    open = False
    
    while open == False:
        address = await websocket.receive()
        try:
            socket = serial.Serial(address, 115200, timeout=10)
            await websocket.send('sensor is connected')
            open = socket.is_open
        except:
            await websocket.send("sensor isn't connected")

        # while True:
        #     data = socket.read(20)
        #     a, w, A = decoded_data(data)

        #     df.loc[len(df.index)] = concatenate([[round(time.perf_counter() - t_start, 2)], a, w, A])
        #     output = json.dumps([
        #         (df[df.columns[i]].tail(50)).to_list() for i in range(len(df.axes[1]))
        #         ])
        #     await websocket.send(output)


if __name__ == "__main__":
    app.run(port=5000)