from bleak import BleakClient
import asyncio
from func.general_operations import di_hz, di_commands

"""Методы для обработки Bluetooth"""

# Калибровка гироскопа и акселерометра для Bluetooth 5.0
async def ble_calibrate_gyr_and_acc(write_uuid, client: BleakClient):
    await client.write_gatt_char(
        write_uuid, 
        di_commands('calibrate gyr and acc'))
    for i in range(3, -1, -1):
        print(f"\rКалибровка гироскопа и акселерометра завершится через {i} сек...", end="")
        await asyncio.sleep(1)
    await client.write_gatt_char(
        write_uuid,
        di_commands('exit calibration mode'))
    print("\nКалибровка гироскопа и акселерометра завершена.\n")  

# Калибровка магнитрометра для Bluetooth 5.0
async def ble_calibrate_magn(write_uuid, client: BleakClient):
    await client.write_gatt_char(
        write_uuid, 
        di_commands('calibrate magn'))
    print('Для калибровки магнитрометра необходимо провернуть датчик по КАЖДОЙ оси (начинать с OZ) на 360 град по 3 раза.')
    while input('Для продолжения введите "y"') != 'y':
        pass
    await client.write_gatt_char(
        write_uuid,
        di_commands('exit calibration mode'))
    print("Калибровка магнитрометра завершена.\n")

# Переключение Algorithm Transition для Bluetooth 5.0 
async def ble_algorithm_transition(write_uuid, client: BleakClient, axis):
    if axis == 6:
        await client.write_gatt_char(
            write_uuid, 
            di_commands('6 algorithm transition'))
        print('Выбран 6-ти степенной алгоритм.')
    elif axis == 9:
        await client.write_gatt_char(
            write_uuid, 
            di_commands('9 algorithm transition'))
        print('Выбран 9-ти степенной алгоритм.')    
    await client.write_gatt_char(
        write_uuid,
        di_commands('save configuration'))

# Изменение частоты обновления данных для Bluetooth 5.0
async def ble_return_rate(write_uuid, client: BleakClient, rate):
    await client.write_gatt_char(
        write_uuid, 
        di_hz(rate))
    print(f'Выбрана частота обновления: {rate} Гц.')
    await client.write_gatt_char(
        write_uuid,
        di_commands('save configuration'))
    print('Частота изменена.')