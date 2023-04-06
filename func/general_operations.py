import pandas as pd


"""Общие для USB и Bluetooth методы"""

# Создание таблицы для записи данных
def create_table():
    df = pd.DataFrame() # Создадим таблицу, куда будем созранять все значения
    df = df.reindex(columns=['t, с', 'aX, м/с2', 'aY, м/с2', 'aZ, м/с2', 'wX, °/с', 'wY, °/с', 'wZ, °/с', 'AX, °', 'AY, °', 'AZ, °',])
    return df


def di_hz(rate):
    # Таблица для команд, изменяющих Гц (стр. 19 - WT901BLECL DataSheet.pdf)
    di_rate = {0.2: b'\xFF\xAA\x03\x01\x00', 0.5: b'\xFF\xAA\x03\x02\x00', 1: b'\xFF\xAA\x03\x03\x00',
                2: b'\xFF\xAA\x03\x04\x00', 5: b'\xFF\xAA\x03\x05\x00', 10: b'\xFF\xAA\x03\x06\x00',
                20: b'\xFF\xAA\x03\x07\x00', 50: b'\xFF\xAA\x03\x08\x00'}
    return di_rate[rate]


# Таблица с командами
def di_commands(key):
    di = {'accelerometer_calibration': b'\xFF\xAA\x01\x01\x00', 'magnetometer_calibration' : b'\xFF\xAA\x01\x07\x00',
        'exit_calibration_mode': b'\xFF\xAA\x01\x00\x00', '6_DOF': b'\xFF\xAA\x24\x01\x00',
        '9_DOF': b'\xFF\xAA\x24\x00\x00', 'save_configuration': b'\xFF\xAA\x00\x00\x00'}
    return di[key]


# Обработка поступающего сигнала
def decoded_data(data): 
    decoded = [int.from_bytes(data[i:i+2], byteorder='little', signed=True) for i in range(2, len(data), 2)]

    ax, ay, az = decoded[0] / 32768.0 * 16, decoded[1] / 32768.0 * 16, decoded[2] / 32768.0 * 16
    wx, wy, wz = decoded[3] / 32768.0 * 2000, decoded[4] / 32768.0 * 2000, decoded[5] / 32768.0 * 2000
    Ax, Ay, Az = decoded[6] / 32768.0 * 180, decoded[7] / 32768.0 * 180, decoded[8] / 32768.0 * 180

    return [ax, ay, az], [wx, wy, wz], [Ax, Ay, Az]    
