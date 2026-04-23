import asyncio
import json
import websockets

WS_URL = "ws://localhost:10000/ws"

SAMPLES = [
    {"Soil_Moisture": 80.0, "Ambient_Temperature": 28.0, "Humidity": 60.0},
    {"Soil_Moisture": 12.0, "Ambient_Temperature": 35.0, "Humidity": 20.0},
    {"Soil_Moisture": 45.0, "Ambient_Temperature": 22.0, "Humidity": 55.0},
    {"Soil_Moisture": 5.0,  "Ambient_Temperature": 40.0, "Humidity": 10.0},
    {"Soil_Moisture": 70.0, "Ambient_Temperature": 18.0, "Humidity": 75.0},
]


async def run():
    async with websockets.connect(WS_URL) as ws:
        for sample in SAMPLES:
            await ws.send(json.dumps(sample))
            response = json.loads(await ws.recv())
            print(f"Input: {sample} -> {response}")

asyncio.run(run())
