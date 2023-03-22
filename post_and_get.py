from quart import Quart, request
from func.serial_ports import serial_ports


app = Quart(__name__)
address = None

# Для отправки доступных адресов
@app.get("/available_ports")
async def ports():
    available_ports = serial_ports()
    return available_ports

# Для приёма выбранного адреса
@app.post("/post")
async def post():
    global address
    address = await request.get_json()
    return [f'input "{address}" accepted.']

@app.get("/chosen_address")
async def chosen_address():
    return [address]
    

if __name__ == "__main__":
    app.run(port=5001)