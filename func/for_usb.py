import serial
import time
from func.general_operations import di_hz, di_commands


# Калибровка гироскопа и акселерометра для USB
def usb_calibrate_gyr_and_acc(socket):
    socket.write(di_commands('accelerometer_calibration'))
    time.sleep(4)
    socket.write(di_commands('exit_calibration_mode'))  


# # Калибровка магнитрометра для USB
# def usb_calibrate_magn(socket):
#     socket.write(di_commands('calibrate magn'))
#     print('Для калибровки магнитрометра необходимо провернуть датчик по КАЖДОЙ оси (начинать с OZ) на 360 град по 3 раза.')
#     while input('Для продолжения введите "y"') != 'y':
#         pass
#     socket.write(di_commands('exit calibration mode'))
#     print("Калибровка магнитрометра завершена.\n")


# Переключение Algorithm Transition для USB
def usb_algorithm_transition(socket, axis):
    socket.write(di_commands(axis))  
    socket.write(di_commands('save_configuration'))


# Изменение частоты обновления данных для USB
def usb_return_rate(socket, rate):
    socket.write(di_hz(rate))
    socket.write(di_commands('save_configuration'))