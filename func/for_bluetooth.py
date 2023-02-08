from bleak import BleakClient
import asyncio
from func.general_operations import di

"""Методы для обработки Bluetooth"""

# Калибровка гироскопа и акселерометра для Bluetooth 5.0
async def ble_calibrate_gyr_and_acc(write_uuid, client: BleakClient):
    await client.write_gatt_char(
        write_uuid, 
        b'\xFF\xAA\x01\x01\x00')
    for i in range(3, -1, -1):
        print(f"\rКалибровка гироскопа и акселерометра завершится через {i} сек...", end="")
        await asyncio.sleep(1)
    await client.write_gatt_char(
        write_uuid,
        b'\xFF\xAA\x01\x00\x00')
    print("\nКалибровка гироскопа и акселерометра завершена.\n")  

# Калибровка магнитрометра для Bluetooth 5.0
async def ble_calibrate_magn(write_uuid, client: BleakClient):
    await client.write_gatt_char(
        write_uuid, 
        b'\xFF\xAA\x01\x07\x00')
    print('Для калибровки магнитрометра необходимо провернуть датчик по КАЖДОЙ оси (начинать с OZ) на 360 град по 3 раза.')
    while input('Для продолжения введите "y"') != 'y':
        pass
    await client.write_gatt_char(
        write_uuid,
        b'\xFF\xAA\x01\x00\x00')
    print("Калибровка магнитрометра завершена.\n")

# Переключение Algorithm Transition для Bluetooth 5.0 
async def ble_algorithm_transition(write_uuid, client: BleakClient, axis):
    if axis == 6:
        await client.write_gatt_char(
            write_uuid, 
            b'\xFF\xAA\x24\x01\x00')
        print('Выбран 6-ти степенной алгоритм.')
    elif axis == 9:
        await client.write_gatt_char(
            write_uuid, 
            b'\xFF\xAA\x24\x00\x00')
        print('Выбран 9-ти степенной алгоритм.')    
    await client.write_gatt_char(
        write_uuid,
        b'\xFF\xAA\x00\x00\x00')

# Изменение частоты обновления данных для Bluetooth 5.0
async def ble_return_rate(write_uuid, client: BleakClient, rate):
    await client.write_gatt_char(
        write_uuid, 
        di(rate))
    print(f'Выбрана частота обновления: {rate} Гц.')
    await client.write_gatt_char(
        write_uuid,
        b'\xFF\xAA\x00\x00\x00')
    print('Частота изменена.')