import serial
import time
import sys
import glob
import serial

from func.general_operations import di_hz, di_commands


# Калибровка гироскопа и акселерометра для USB
def usb_calibrate_gyr_and_acc(socket):
    socket.write(di_commands('accelerometer_calibration'))
    time.sleep(4)
    socket.write(di_commands('exit_calibration_mode'))  


# Переключение Algorithm Transition для USB
def usb_algorithm_transition(socket, axis):
    socket.write(di_commands(axis))  
    socket.write(di_commands('save_configuration'))


# Изменение частоты обновления данных для USB
def usb_return_rate(socket, rate):
    socket.write(di_hz(rate))
    socket.write(di_commands('save_configuration'))
    
    
# Поиск подключённых usb устройств
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result    
