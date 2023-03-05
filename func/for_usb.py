import serial
import time
from func.general_operations import di_hz, di_commands

# Подключение к USB
def connection_to_usb(device, calibrate_gyr_and_acc, calibrate_magn, algorithm_transition, rate):
    # Create the client socket
    port = device[1]
    baud = 115200
    socket = serial.Serial(port, baud, timeout=5)
    print("Connected: True.")
    if calibrate_gyr_and_acc:  # Калибровка
        usb_calibrate_gyr_and_acc(socket)
    if calibrate_magn:
        usb_calibrate_magn(socket) 
    if algorithm_transition != None:   # Переключение алгоритма
        usb_algorithm_transition(socket, algorithm_transition)
    if rate != None:   # Выбор частоты передачи данных
        usb_return_rate(socket, rate)
    return socket

# Калибровка гироскопа и акселерометра для USB
def usb_calibrate_gyr_and_acc(socket):
    socket.write(di_commands('calibrate gyr and acc'))
    for i in range(3, -1, -1):
        print(f"\rКалибровка гироскопа и акселерометра завершится через {i} сек...", end="")
        time.sleep(1)
    socket.write(di_commands('exit calibration mode'))    
    print("\nКалибровка гироскопа и акселерометра завершена.\n")  

# Калибровка магнитрометра для USB
def usb_calibrate_magn(socket):
    socket.write(di_commands('calibrate magn'))
    print('Для калибровки магнитрометра необходимо провернуть датчик по КАЖДОЙ оси (начинать с OZ) на 360 град по 3 раза.')
    while input('Для продолжения введите "y"') != 'y':
        pass
    socket.write(di_commands('exit calibration mode'))
    print("Калибровка магнитрометра завершена.\n")

# Переключение Algorithm Transition для USB
def usb_algorithm_transition(socket, axis):
    if axis == 6:
        socket.write(di_commands('6 algorithm transition'))
        print('Выбран 6-ти степенной алгоритм.')
    elif axis == 9:
        socket.write(di_commands('9 algorithm transition'))
        print('Выбран 9-ти степенной алгоритм.')    
    socket.write(di_commands('save configuration'))

# Изменение частоты обновления данных для USB
def usb_return_rate(socket, rate):
    socket.write(di_hz(rate))
    print(f'Выбрана частота обновления: {rate} Гц.')
    socket.write(di_commands('save configuration'))
    print('Частота изменена.')