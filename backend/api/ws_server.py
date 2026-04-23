import asyncio
import websockets
from backend.controllers.voice_controller import process_voice

async def handler(websocket):
    async for message in websocket:
        response = await process_voice({"audio": message})
        await websocket.send(str(response))

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()