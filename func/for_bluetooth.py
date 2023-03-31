# import asyncio
from bleak import BleakScanner
# import nest_asyncio
# import time
# import os


# Поиск устройств по bluetooth  - эти части НЕ НУЖНЫ при вызове в output.py 
# def device_search():
    # os.system("rfkill unblock bluetooth")
    # time.sleep(0.5)
    # nest_asyncio.apply()

async def run():
    devices = await BleakScanner.discover(timeout=1)
    d = [dev.address for dev in devices if 'WT901' in dev.name]
    return d
     
    # loop = asyncio.get_event_loop()
    # return loop.run_until_complete(run())