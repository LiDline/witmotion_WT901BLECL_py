# WITMOTION WT901BLECL
Здесь представлено небольшое web-приложение для использования датчика WT901BLECL (через USB и bluetooth) средствами Python. Вся информация о датчике находится [тут](https://github.com/WITMOTION/WT901BLECL). Помимо этой документации, советую посмотреть документацию на используемый в датчике сенсор [WT901](https://images-na.ssl-images-amazon.com/images/I/B11fVGszLsS.pdf). В репозитории 3 ветки: 
1. master - реализация на plotly dash (на данный момент полностью реализован метод usb, частично bluetooth - нет калибровки);
2. draft - реализация на python (100% реализация);
3. react - реализация на react (на данный момент реализовано только чтение с usb).

## 1 Состав ветки на dash
1. папка assets - .css файлы;
2. папка pages - разбиение приложения на 3 основных страницы (стандартный синтаксис dash);
3. папка func - необходимые функции и компоненты dash:
- папка components - компоненты фронта, а также callback;
- for_bluetooth.py - необходимые методы для подключения по Bluetooth;
- for_usb.py - необходимые методы для подключения по usb;
- general_operations.py - общие методы для подключение по Bluetooth и usb;
- graph.js - отрисовка графика.
4. app.py - фронт;
5. output.py - бэк;

## 2 Запуск программы
Запуск программы осуществляется через 'app.py'.
```
python3 app.py
```
 Приложение будет доступно в браузере по ссылке: http://127.0.0.1:8050/.

## 3 Используемые библиотеки
Используемые библиотеки:
- asyncio;
- pybluez;
- serial;
- plotly;
- datetime;
- numpy;
- dash;
- requests;
- os;
- re;
- time;
- sys;
- json;
- sys;
- dash_extensions;
- dash_bootstrap_components;
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
где /dev/ttyUSB0 - результат предыдущей команды. При переподключении датчика придётся вводить эту команду каждый раз. Если Вам это не нужно, введите следующую строку.
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


### P.s. 
Реализация live-data на dash в разы сложнее и объёмнее, чем просто на .py или react.