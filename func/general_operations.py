import pandas as pd
from numpy import zeros, vstack, concatenate
import time

"""Общие для USB и Bluetooth методы"""

# Создание таблицы для записи данных
def create_table():
    df = pd.DataFrame() # Создадим таблицу, куда будем созранять все значения
    df = df.reindex(columns=['t, с', 'aX, м/с2', 'aY, м/с2', 'aZ, м/с2', 'wX, °/с', 'wY, °/с', 'wZ, °/с', 'AX, °', 'AY, °', 'AZ, °',])
    return df

# Создание необходимых констант
def init_table():
# Создадим массивы для графиков
    aa = zeros(3)
    ww = zeros(3)
    AA = zeros(3)

    df = create_table()    

    print('Идёт снятие данных.', 'Для завершения нажмите Interrupt.')

    counter = 0
    
    t_start = time.perf_counter()
    t = []

    return counter, t_start, t, aa, ww, AA, df

# Обрабока полученных данных для графиков и таблицы результатов
def data_processing(fig, a, w, A, aa, ww, AA, t, t_start, x_label_size, counter, df):
    if all([a is not None, w is not None, A is not None]):
        t.append(time.perf_counter() - t_start)
        aa = vstack((aa, a))
        ww = vstack((ww, w))
        AA = vstack((AA, A))
        with fig.batch_update():  
            # Меняем заголовки sub'ов (записываем текущие характеристики)  
            fig.layout.annotations[0].update(
                                        text=(f"Линейные ускорения (aX = {'{0: <4}'.format(round(a[0], 1))}, aY = {'{0: <4}'.format(round(a[1], 1))}, aZ = {'{0: <4}'.format(round(a[2], 1))})"))
            fig.layout.annotations[1].update(
                                        text=(f"Угловые скорости (wX = {'{0: <4}'.format(round(w[0]))}, wY = {'{0: <4}'.format(round(w[1]))}, wZ = {'{0: <4}'.format(round(w[2]))})"))
            fig.layout.annotations[2].update(
                                        text=(f"Углы (AX = {'{0: <5}'.format(round(A[0]))}, AY = {'{0: <5}'.format(round(A[1]))}, AZ = {'{0: <5}'.format(round(A[2]))})"))

            for i in range(3):
                fig.data[i].y = aa[:,i]
                fig.data[i].x = t
                fig.data[i+3].y = ww[:,i]
                fig.data[i+3].x = t
                fig.data[i+6].y = AA[:,i]
                fig.data[i+6].x = t  
        if len(aa) > x_label_size:  # Ограничение по отображаемым данным
            t  = t[-x_label_size:]
            aa = aa[-x_label_size:]
            ww = ww[-x_label_size:] 
            AA = AA[-x_label_size:]

        df.loc[counter,:] = concatenate([[round(time.perf_counter() - t_start, 2)], a, w, A]) 
        counter += 1    

    return t, aa, ww, AA, counter, df

def di(rate):
    # Таблица для команд, изменяющих Гц (стр. 19 - WT901BLECL DataSheet.pdf)
    di_rate = {0.2: b'\xFF\xAA\x03\x01\x00', 0.5: b'\xFF\xAA\x03\x02\x00', 1: b'\xFF\xAA\x03\x03\x00',
                2: b'\xFF\xAA\x03\x04\x00', 5: b'\xFF\xAA\x03\x05\x00', 10: b'\xFF\xAA\x03\x06\x00',
                20: b'\xFF\xAA\x03\x07\x00', 50: b'\xFF\xAA\x03\x08\x00'}
    return di_rate[rate]

# Обработка поступающего сигнала
def decoded_data(data): 
    decoded = [int.from_bytes(data[i:i+2], byteorder='little', signed=True) for i in range(2, len(data), 2)]

    ax, ay, az = decoded[0] / 32768.0 * 16, decoded[1] / 32768.0 * 16, decoded[2] / 32768.0 * 16
    wx, wy, wz = decoded[3] / 32768.0 * 2000, decoded[4] / 32768.0 * 2000, decoded[5] / 32768.0 * 2000
    Ax, Ay, Az = decoded[6] / 32768.0 * 180, decoded[7] / 32768.0 * 180, decoded[8] / 32768.0 * 180

    return [ax, ay, az], [wx, wy, wz], [Ax, Ay, Az]    