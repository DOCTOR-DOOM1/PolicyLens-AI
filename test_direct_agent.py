import os
import sys
import asyncio
import aiohttp
from dotenv import load_dotenv
load_dotenv()

from livekit import rtc
from livekit.api import AccessToken, VideoGrants
from livekit.agents import AgentSession, Agent
from livekit.plugins import openai, silero, cartesia

async def run_direct():
    print("Generating token...")
    token = AccessToken(
        os.getenv('LIVEKIT_API_KEY'),
        os.getenv('LIVEKIT_API_SECRET')
    ).with_identity("AI_Agent").with_name("PolicyLens AI").with_grants(VideoGrants(room_join=True, room="policylens-room")).to_jwt()
    
    print("Connecting to room...")
    room = rtc.Room()
    await room.connect(os.getenv("LIVEKIT_URL"), token)
    print("Connected!")
    
    stt = openai.STT(
        model="whisper-large-v3",
        base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get("GROQ_API_KEY")
    )
    llm_engine = openai.LLM(
        model="llama-3.3-70b-versatile",
        base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get("GROQ_API_KEY")
    )
    session_http = aiohttp.ClientSession()
    tts = cartesia.TTS(
        api_key=os.environ.get("CARTESIA_API_KEY"),
        model="sonic-multilingual",
        http_session=session_http
    )
    session = AgentSession(
        vad=silero.VAD.load(), 
        stt=stt,
        llm=llm_engine,
        tts=tts,
    )
    policy_agent = Agent(
        instructions="You are PolicyLens AI, a helpful voice assistant for Indian citizens. Keep your answers brief, conversational, and easy to understand."
    )
    print("Starting session...")
    await session.start(room=room, agent=policy_agent)
    
    print("Generating reply...")
    try:
        await session.generate_reply(
            instructions="Greet the user by saying: Namaste! I am PolicyLens AI. How can I help you with government schemes today?"
        )
        print("Reply generated and audio sent.")
    except Exception as e:
        import traceback
        traceback.print_exc()

    await asyncio.sleep(5)
    await room.disconnect()
    print("Done")

if __name__ == "__main__":
    asyncio.run(run_direct())
