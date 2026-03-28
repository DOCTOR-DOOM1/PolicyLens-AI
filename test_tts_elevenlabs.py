import os
import asyncio
import aiohttp
from dotenv import load_dotenv
load_dotenv()

from livekit.plugins import elevenlabs

async def test_elevenlabs():
    session = aiohttp.ClientSession()
    try:
        tts = elevenlabs.TTS(
            api_key=os.environ.get("ELEVENLABS_API_KEY"),
            http_session=session
        )
        print("Instantiated ElevenLabs TTS")
        stream = tts.synthesize("Hello, this is ElevenLabs testing in Hindi: नमस्ते.")
        async for audio in stream:
            print("Received audio chunk:", len(audio.data))
            break
        print("Success.")
    except Exception as e:
        print("Error:", e)
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(test_elevenlabs())
