from bleak import BleakClient
import asyncio
from func.general_operations import init_table, data_processing, decoded_data
from func.for_bluetooth import ble_calibrate_gyr_and_acc, ble_calibrate_magn, ble_algorithm_transition, ble_return_rate
from func.for_usb import connection_to_usb

class WT901BLE():
    notify_uuid = "0000ffe4-0000-1000-8000-00805f9a34fb" # UUID для считывания (Одинаковы для WT901BLE)
    write_uuid = "0000ffe9-0000-1000-8000-00805f9a34fb" # UUID для записи

    def __init__(self, fig, device, calibrate_gyr_and_acc, calibrate_magn, algorithm_transition, rate = None, x_label_size = 50):
        self.fig = fig
        self.device = device
        self.calibrate_gyr_and_acc = calibrate_gyr_and_acc
        self.calibrate_magn = calibrate_magn
        self.algorithm_transition = algorithm_transition
        self.rate = rate
        self.x_label_size = x_label_size
        self.current_data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Для того, чтобы вытащить данные из start_notify
    def data(self):    
        return self.current_data   

    def table(self, df):
        self.table = df    
#_________________________________________________________________________________________________________________________________

    """Часть с Bluetooth"""

    # Приём пакетов по Bluetooth и их обработка (По Bluetooth WT901BLE по умолчанию отправляет пакет в 20 байтов)
    def _notification_handler(self, sender, data: bytearray):
            header_bit = data[0]
            assert header_bit == 0x55
            flag_bit = data[1] # 0x51 or 0x71
            assert flag_bit == 0x61 or flag_bit == 0x71
            self.current_data = decoded_data(data)

    # Считывание по Bluetooth
    async def bluetooth_run_async(self):
        async with BleakClient(self.device[1]) as client:
            x = client.is_connected
            print("Connected: {0}.".format(x))

            if self.calibrate_gyr_and_acc:  # Калибровка
                await ble_calibrate_gyr_and_acc(self.write_uuid, client)
            if self.calibrate_magn:
                await ble_calibrate_magn(self.write_uuid, client) 

            if self.algorithm_transition != None:   # Переключение алгоритма
                await ble_algorithm_transition(self.write_uuid, client, self.algorithm_transition)

            if self.rate != None:   # Выбор частоты передачи данных
                await ble_return_rate(self.write_uuid, client, self.rate)    

            counter, t_start, t, aa, ww, AA, df = init_table()

            while True:
                await client.start_notify(self.notify_uuid, self._notification_handler)

                a, w, A = self.current_data[0], self.current_data[1], self.current_data[2]
                t, aa, ww, AA, counter, df = data_processing(self.fig, a, w, A, aa, ww, AA, t, t_start, 
                                                            self.x_label_size, counter, df)
                self.table = df
                # await asyncio.sleep(0.1) # А надо ли?
#_________________________________________________________________________________________________________________________________
                
    """Часть с USB"""

    def usb_run(self):
        socket = connection_to_usb(self.device, self.calibrate_gyr_and_acc, self.calibrate_magn, 
                                    self.algorithm_transition, self.rate)
        counter, t_start, t, aa, ww, AA, df = init_table()
        while True:
            data = socket.read(20)
            a, w, A = decoded_data(data)
            
            t, aa, ww, AA, counter, df = data_processing(self.fig, a, w, A, aa, ww, AA, t, t_start, self.x_label_size, counter, df)
            self.table = df