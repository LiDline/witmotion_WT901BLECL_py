import json
import time
from bleak import BleakScanner
from numpy import concatenate
from quart import websocket


from func.general_operations import create_table, decoded_data


async def run():
    devices = await BleakScanner.discover(timeout=1)
    d = [dev.address for dev in devices if 'WT901' in dev.name]
    return d


class Bluetooth():
    # UUID для считывания (Одинаковы для WT901BLE)
    notify_uuid = "0000ffe4-0000-1000-8000-00805f9a34fb"
    write_uuid = "0000ffe9-0000-1000-8000-00805f9a34fb"  # UUID для записи

    current_data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def __init__(self, command):
        self.command = command

    # Для того, чтобы вытащить данные из start_notify
    def data(self):
        return self.current_data

    def _notification_handler(self, sender, data: bytearray):
        header_bit = data[0]
        assert header_bit == 0x55
        flag_bit = data[1]  # 0x51 or 0x71
        assert flag_bit == 0x61 or flag_bit == 0x71
        self.current_data = decoded_data(data)

    async def bluetooth_run_async(self, client):
        t_start = time.perf_counter()
        df = create_table()

        while self.command:
            await client.start_notify(self.notify_uuid, self._notification_handler)
            a, w, A = self.current_data[0], self.current_data[1], self.current_data[2]
            df.loc[len(df.index)] = concatenate(
                [[round(time.perf_counter() - t_start, 2)], a, w, A])
    
            output = json.dumps([
                (df[df.columns[i]].tail(50)).to_list() for i in range(len(df.axes[1]))
            ])
            print(a)
            await websocket.send(output)
