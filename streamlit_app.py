import streamlit as st
import time
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="PolicyLens AI - Control Center", 
    page_icon="🇮🇳", 
    layout="wide"
)

# --- Header ---
st.title("🎙️ PolicyLens AI: Real-Time RAG Monitor")
st.markdown("**Status:** 🟢 LiveKit Voice Engine Active | 📚 ChromaDB Local Vector Store Connected")
st.divider()

# --- Dashboard Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Voice Transcript")
    # Reads the live transcript written by your voice_agent.py
    try:
        with open("live_transcript.txt", "r") as f:
            logs = f.read()
        st.text_area("Agent & User Audio Stream", logs, height=400)
    except FileNotFoundError:
        st.info("Waiting for voice stream to start... Speak into the LiveKit Playground.")

with col2:
    st.subheader("🧠 RAG Source Grounding")
    st.info("Querying 2,200 Local Government PDFs via all-MiniLM-L6-v2")
    
    # Reads the exact PDF chunk pulled by Langchain
    try:
        with open("rag_sources.txt", "r") as f:
            sources = f.read()
        st.success(f"**Latest Document Retrieved:**\n\n{sources}")
    except FileNotFoundError:
        st.warning("Awaiting semantic search trigger...")

# --- Hackathon Auto-Refresh Trick ---
# This forces the Streamlit UI to update every 2 seconds to show new text
time.sleep(2)
st.rerun()