from quart import Quart, request
from func.serial_ports import serial_ports
import serial


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
    global address
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
    return ['Поехали']

@app.get("/executed_order")
async def executed_order():
    return [command]


if __name__ == "__main__":
    app.run(port=5001,
            )