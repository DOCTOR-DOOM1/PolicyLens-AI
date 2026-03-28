import os
import sys
import asyncio
from dotenv import load_dotenv

# Load the keys into memory forcefully overriding old cached keys from streamlit
load_dotenv(override=True)
try:
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("OPENAI_API_KEY="):
                os.environ["OPENAI_API_KEY"] = line.split("=", 1)[1].strip().strip('""')
except Exception:
    pass

from livekit import rtc
from livekit.api import AccessToken, VideoGrants
from livekit.agents.voice import AgentSession, Agent
from livekit.plugins import openai, silero, cartesia
import aiohttp

async def run_agent():
    print("Generating token for PolicyLens AI Agent...")
    token = AccessToken(
        os.getenv('LIVEKIT_API_KEY'),
        os.getenv('LIVEKIT_API_SECRET')
    ).with_identity("AI_Agent").with_name("PolicyLens AI").with_grants(VideoGrants(room_join=True, room="policylens-room")).to_jwt()
    
    print("Connecting to room...")
    room = rtc.Room()
    await room.connect(os.getenv("LIVEKIT_URL"), token)
    print("Agent Connected Successfully!")

    # Start plugins
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
    
    http_session = aiohttp.ClientSession()

    tts = cartesia.TTS(
        api_key=os.environ.get("CARTESIA_API_KEY"),
        model="sonic-multilingual",
        http_session=http_session,
    )


    # Use Voice Session with optimized VAD
    session = AgentSession(
        vad=silero.VAD.load(min_silence_duration=0.5),
        stt=stt,
        llm=llm_engine,
        tts=tts,
    )
    
    agent = Agent(
        instructions=(
            "You are PolicyLens AI, a specialized voice assistant for Indian citizens focused ONLY on government policies, schemes, and scholarships.\n"
            "CRITICAL RULES:\n"
            "1. Domain Restriction: If the user asks about ANYTHING outside of general greetings, government policies, or scholarships (e.g., code, math, weather, history, pop culture, general trivia), you MUST refuse to answer. Politely reply with: 'I am specialized in PolicyLens. I can only provide you with data regarding government policies and scholarships.'\n"
            "2. Keep your answers extremely brief, conversational, and highly accessible.\n"
            "3. Always reply natively in the same language the user speaks to you."
        )
    )

    # Start the agent processing loops
    await session.start(room=room, agent=agent)

    # Greet the user automatically
    try:
        await session.generate_reply(
            instructions="Greet the user warmly by saying: Namaste! I am PolicyLens AI. How can I help you today?"
        )
    except Exception as e:
        print("Initial reply error:", e)

    # Keep the job context open indefinitely
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run_agent())