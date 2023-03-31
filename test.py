from bleak import BleakClient
import nest_asyncio
import asyncio


async def bluetooth_run_async():
    async with BleakClient('DB:EE:85:7F:44:09') as client:
        x = client.is_connected
        print("Connected: {0}.".format(x))

# # nest_asyncio.apply()
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.run(bluetooth_run_async()))

