import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from livekit.plugins import openai

async def test_openai_tts():
    try:
        tts = openai.TTS(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model="tts-1",
            voice="alloy"
        )
        print("Instantiated OpenAI TTS")
        stream = tts.synthesize("Hello, this is OpenAI testing.")
        async for audio in stream:
            print("Received audio chunk:", len(audio.data))
            break
        print("Success.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(test_openai_tts())
