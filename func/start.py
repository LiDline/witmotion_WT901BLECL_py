import time
import os
from func.WT901BLE import WT901BLE
import nest_asyncio
import asyncio

def start(fig, device, calibrate_gyr_and_acc = False, calibrate_magn = False, algorithm_transition = None, 
        rate = None, x_label_size = 50):

    sensor = WT901BLE(fig, device, calibrate_gyr_and_acc, calibrate_magn, algorithm_transition, rate, x_label_size)
        
    try:
        if device[0] == 'usb':
            sensor.usb_run()
        elif device[0] == 'bluetooth':
            os.system("rfkill unblock bluetooth")
            time.sleep(0.25)   # Есил Bluetooth был выключен, то без паузы будет ошибка
            print('bluetooth запущен.')

            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.run(sensor.bluetooth_run_async()))
            
    except KeyboardInterrupt:  
        print('Считывание завершено.')
        sensor.table.to_csv('WT901BLE_res.csv')
        print('Таблица, под именем "WT901BLE_res.csv", сохранена в папке проекта.')    