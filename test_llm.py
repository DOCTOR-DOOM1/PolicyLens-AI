import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from livekit.plugins import openai

async def test_llm():
    try:
        llm_engine = openai.LLM(
            model="llama-3.3-70b-versatile",
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ.get("GROQ_API_KEY") # Fixed: Now looks for the name
        )
        print("Instantiated LLM")
        
        from livekit.agents.llm import ChatContext, ChatMessage
        ctx = ChatContext()
        ctx.messages.append(ChatMessage.create(text="Say hello.", role="user"))
        
        response = await llm_engine.chat(chat_ctx=ctx)
        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="")
        print("\nSuccess.")
    except Exception as e:
        print("\nError:", e)

if __name__ == "__main__":
    asyncio.run(test_llm())
