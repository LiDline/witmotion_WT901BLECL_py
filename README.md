# WITMOTION WT901BLECL with Python
Здесь представлено небольшое web-приложение для использования датчика WT901BLECL (через USB и bluetooth) средствами Python. Вся информация о датчике находится [тут](https://github.com/WITMOTION/WT901BLECL). Помимо этой документации, советую посмотреть документацию на используемый в датчике сенсор [WT901](https://images-na.ssl-images-amazon.com/images/I/B11fVGszLsS.pdf). В репозитории 2 ветки: 
1. master - реализация на plotly [dash](https://dash.plotly.com/installation) (баг: кривая работа поля выбора доступных датчиков. Решение: не нажимайте сразу кнопку Start);
2. draft - реализация на python.

## 1 Состав проекта
1. Папка func, где лежат используемые функции.
    - device_search.py - поиск ближайших Bluetooth устройств.
    - for_bluetooth.py - необходимые методы для использования датчика через Bluetooth.
    - for_usb.py - необходимые методы для использования датчика через USB.
    - general_operations.py - общие для Bluetooth и USB методы (такие как создание таблицы, запись данных в график...)
    - graph_settings.py - настройки отображаемого в 'WT901BLE.ipynb' графика.
    - main.py - вызов экземпляра класса WT901BLE.
    - WT901BLE.py - класс обработки поступающих данных.
    - graph.py - создание и оформление графика.
2. WT901BLE.ipynb - блокнот с программой для обработки и визуализации данных с датчика через USB/Bluetooth.

## 2 Запуск программы
Запуск осуществляется в блокноте 'WT901BLE.ipynb'. Для запуска Вам необходимо узнать адресс Вашего датчика, Вы можете это сделать, выполнив ячейку с:
```python
device_search()
```
Для начала считывания внесите изменения (по желанию) в параметры и выполните ячейку:
```python
start(fig, # Запись графика, вызванного выше
    device, # Ваше устройство, спиcок из [устройства считывания и MAC]
    calibrate_gyr_and_acc = False, # Калибровка гиро и акселерометра: True/False
    calibrate_magn = False, # Калибровка магнетрометра: True/False
    algorithm_transition = None, # По умолчанию 9, советую сразу ставить 6
    rate = None, # Частота считывания, для WT901BLE: 0.2, 0.5, 1, 2, 5, 10 (default), 20, 50 [Гц]
    x_label_size = 50 # Кол-во точек на графике
    ) 
```

## 3 Используемые библиотеки
Используемые библиотеки:
- asyncio;
- nest_asyncio;
- pybluez;
- pyserial;
- plotly;
- datetime;
- numpy;
- pandas.
____
Все используемые библиотеки указаны в файле requirements.txt. Для быстрой установки отсутствующих библиотек в терминале выполните: 
```
pip install -r requirements.txt
```
## 4 Замечания

### 4.1 Для запуска на Ubuntu через USB:
Перед запуском скрипта в блокноте узнайте куда подключается датчик: 
```
sudo dmesg -wH
```
Затем пропишите: 
```
sudo chmod a+rw /dev/ttyUSB0
```
где /dev/ttyUSB0 - результат предыдущей команды. При переподключении датчика придётся вводить эту команду каждый раз. Если Вам это не нужно, введите следующую строку и перезагрузите компьютер:
```
 sudo usermod -a -G dialout $USER 
```

### 4.2 Документация
Если Вам необходимо изменить конфигурацию датчика, то советую сразу смотреть на документацию встроенного сенсора [WT901](https://images-na.ssl-images-amazon.com/images/I/B11fVGszLsS.pdf). В "родной" документации много чего не хватает.

### 4.3 Калибровка датчика

1. Калибровка акселерометра и гироскопа происходит в течение 3-х секунд после отправки команды (никаких сложностей, просто не трогайте его).
2. Калбировка магнитрометра представляет из себя вращение датчика вокруг своих осей по 3 раза (см. [видео](https://youtu.be/smi2uePvC-Q?t=104))

### 4.4 Сложности

У данного датчика (по умолчанию) позиционирование просиходит путём считывания данных с 9-ти степеней (по осям XYZ: 3 акселерометра, 3 гироскопа, 3 магнитометра). До калибровки магнитометра угол oZ всегда давал одно значение. После калибровки угол oZ работает адекватно ДО ЛЮБОГО резкого линейного толчка (~ 1g) датчика. Брак это или нет, мне не известно. Настоятельно советую забыть про магнитометр и СРАЗУ переключать датчик на 6 степеней.

## 5. Другая версия

Помимо этого существует [репозиторий](https://github.com/LiDline/witmotion_wt901blecl_ts), где данное web-приложение реализовано на react.