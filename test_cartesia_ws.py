import os
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()

async def test_ws():
    api_key = os.environ.get("CARTESIA_API_KEY")
    url = f"wss://api.cartesia.ai/tts/websocket?api_key={api_key}&cartesia_version=2024-06-10"
    print("Connecting to Cartesia WSS...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(url) as ws:
                print("Connected! WSS works!")
                await ws.close()
    except Exception as e:
        print("Raw WS Exception:", repr(e))

if __name__ == "__main__":
    asyncio.run(test_ws())
