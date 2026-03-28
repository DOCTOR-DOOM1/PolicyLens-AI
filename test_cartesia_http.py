import os
import asyncio
import aiohttp
import json
from dotenv import load_dotenv

load_dotenv()

async def test_http():
    api_key = os.environ.get("CARTESIA_API_KEY")
    url = "https://api.cartesia.ai/tts/bytes"
    headers = {
        "X-API-Key": api_key,
        "Cartesia-Version": "2024-06-10"
    }
    payload = {
        "model_id": "sonic-multilingual",
        "transcript": "Hello, testing testing.",
        "voice": {
            "mode": "id",
            "id": "a0e99841-438c-4a64-b679-ae501e7d6091"
        },
        "output_format": {
            "container": "raw",
            "encoding": "pcm_s16le",
            "sample_rate": 24000
        }
    }
    print("Connecting to Cartesia HTTPS POST...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                print("Status:", resp.status)
                body = await resp.text()
                print("Body:", body[:200])
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_http())
