import asyncio
import time
from bleak import BleakClient, BleakScanner


from func.general_operations import decoded_data, di_commands, di_hz


"""Методы для обработки Bluetooth"""

# UUID для считывания (Одинаковы для WT901BLE)
notify_uuid = "0000ffe4-0000-1000-8000-00805f9a34fb"
def write_uuid_func():
    write_uuid = "0000ffe9-0000-1000-8000-00805f9a34fb"  # UUID для записи
    return write_uuid

# Поиск ближайших датчиков
async def run():
    devices = await BleakScanner.discover(timeout=1)
    d = [dev.address for dev in devices if 'WT901' in dev.name]
    return d


# Калибровка гироскопа и акселерометра для Bluetooth 5.0
async def ble_calibrate_gyr_and_acc(client: BleakClient):
    await client.write_gatt_char(
        write_uuid_func(),
        di_commands('accelerometer_calibration'))
    await asyncio.sleep(4)
    await client.write_gatt_char(
        write_uuid_func(),
        di_commands('exit_calibration_mode'))


# Переключение Algorithm Transition для Bluetooth 5.0 
async def ble_algorithm_transition(client: BleakClient, axis):
    await client.write_gatt_char(
        write_uuid_func(), 
        di_commands(axis))
    await client.write_gatt_char(
        write_uuid_func(),
        di_commands('save_configuration'))


# Изменение частоты обновления данных для Bluetooth 5.0
async def ble_return_rate(client: BleakClient, rate):
    await client.write_gatt_char(
        write_uuid_func(), 
        di_hz(rate))
    await client.write_gatt_char(
        write_uuid_func(),
        di_commands('save_configuration'))
    

# Класс для принятия и обработки данных
class Bluetooth():
    current_data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def __init__(self, rate):
        self.rate = rate

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
        await client.start_notify(notify_uuid, self._notification_handler)
        a, w, A = self.current_data[0], self.current_data[1], self.current_data[2]

        # Иначе шлёт данные по websocket каждые 0.01 сек
        time.sleep(1/self.rate)

        return a, w, A
