import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from livekit.plugins import cartesia

async def test_tts():
    try:
        import aiohttp
        http_session = aiohttp.ClientSession()
        tts = cartesia.TTS(
            api_key=os.environ.get("CARTESIA_API_KEY"),
            model="sonic-multilingual",
            http_session=http_session,
        )
        print("Instantiated Cartesia TTS with default voice")
        stream = tts.synthesize("Hello, testing testing.")
        async for audio in stream:
            print("Received audio chunk:", len(audio.data))
            break
        print("Success.")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_tts())
