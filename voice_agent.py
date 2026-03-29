import os
import asyncio

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from dotenv import load_dotenv

load_dotenv(override=True)

from livekit.agents import cli, WorkerOptions, JobContext, Agent
from livekit.agents.voice import AgentSession
from livekit.plugins import openai, silero, cartesia

async def entrypoint(ctx: JobContext):
    """Main entrypoint called by the LiveKit worker for each room job."""
    print(f"[PolicyLens] Agent job received. Connecting to room: {ctx.room.name}")

    # Connect to the assigned LiveKit room
    await ctx.connect()
    print("[PolicyLens] Connected to room successfully!")

    tts_plugin = cartesia.TTS(
        api_key=os.environ.get("CARTESIA_API_KEY"),
        model="sonic-multilingual",
    )

    # Build the voice pipeline
    session = AgentSession(
        vad=silero.VAD.load(min_silence_duration=0.5),
        stt=openai.STT(
            model="whisper-large-v3",
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ.get("GROQ_API_KEY"),
        ),
        llm=openai.LLM(
            model="llama-3.3-70b-versatile",
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ.get("GROQ_API_KEY"),
        ),
        tts=tts_plugin,
    )

    agent = Agent(
        instructions=(
            "You are PolicyLens AI, a specialized voice assistant for Indian citizens focused ONLY on government policies, schemes, and scholarships.\n"
            "CRITICAL RULES:\n"
            "1. Domain: If the user asks anything outside government policies/scholarships/greetings, politely say: 'I am specialized in PolicyLens. I can only help with government policies and scholarships.'\n"
            "2. Keep answers brief, friendly, and highly accessible.\n"
            "3. ENGLISH ONLY: You must ONLY speak and reply in English. If the user speaks Hindi, Marathi, Tamil, or any other language, politely tell them 'I am currently operating in English-only mode. How can I help you today?' in English."
        )
    )

    # Start the session — this wires room audio to the pipeline
    await session.start(room=ctx.room, agent=agent)
    print("[PolicyLens] Session started. Sending greeting...")

    # Trigger an opening greeting
    await session.generate_reply(
        instructions="Greet the user warmly: 'Namaste! I am PolicyLens AI. How can I help you with government policies today?'"
    )

    print("[PolicyLens] Agent is live and listening.")

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Voice Agent is Live")
        
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
    def log_message(self, format, *args):
        # Silencing massive health check spam from the load balancer
        pass

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 7860), HealthCheckHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Start the dummy server in a background daemon thread for Hugging Face Spaces
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            # Agent will accept jobs from any room — the UI token
            # specifies 'policylens-room' so they'll be matched automatically
        )
    )