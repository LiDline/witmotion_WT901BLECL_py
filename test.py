import serial

res = serial.Serial('/dev/ttyUSB0', 115200, timeout=10)
# res = type(res)

print(res.__dict__)