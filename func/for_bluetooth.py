import time
from bleak import BleakScanner


from func.general_operations import decoded_data


async def run():
    devices = await BleakScanner.discover(timeout=1)
    d = [dev.address for dev in devices if 'WT901' in dev.name]
    return d


class Bluetooth():
    # UUID для считывания (Одинаковы для WT901BLE)
    notify_uuid = "0000ffe4-0000-1000-8000-00805f9a34fb"
    write_uuid = "0000ffe9-0000-1000-8000-00805f9a34fb"  # UUID для записи

    current_data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

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
        await client.start_notify(self.notify_uuid, self._notification_handler)
        a, w, A = self.current_data[0], self.current_data[1], self.current_data[2]
        
        time.sleep(0.1) # Иначе шлёт данные по websocket каждые 0.01 сек
        
        return a, w, A
        
