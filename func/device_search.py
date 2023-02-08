import asyncio
from bleak import BleakScanner
import nest_asyncio
import time
import os

def device_search():
    os.system("rfkill unblock bluetooth")
    time.sleep(0.5)
    nest_asyncio.apply()

    async def run():
        devices = await BleakScanner.discover()
        for d in devices:
            if 'WT901' in d.name:
                print(f"address: {d.address}, name: {d.name}")
     
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())