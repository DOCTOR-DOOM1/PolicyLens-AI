# 🏛️ PolicyLens AI

> **AI-powered platform that helps Indian citizens discover, understand, and apply for government schemes and scholarships — in their own language.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge)](https://groq.com)
[![LiveKit](https://img.shields.io/badge/LiveKit-Voice-blueviolet?style=for-the-badge)](https://livekit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 🎯 Problem Statement

Over **2,500+ central and state government schemes** exist in India — but most citizens never benefit from them due to:
- Language barriers and complex bureaucratic jargon
- Difficulty finding schemes relevant to their specific profile
- No accessible, unified interface to search and compare policies

**PolicyLens AI solves all of this.**

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Intelligent Eligibility Checker** | Fill in your profile (age, income, occupation, state, category) and our RAG engine semantically matches you against thousands of local policy documents |
| 🤖 **AI Assistant (Text)** | Ask any question about government schemes in plain language — powered by Llama 3.3 70B via Groq |
| 🎙️ **Voice AI Agent** | Real-time voice conversation in English, Hindi, Marathi, and Tamil using LiveKit + Cartesia TTS + Groq Whisper STT |
| ⚖️ **Policy Comparison Tool** | Compare any two schemes side-by-side (e.g., PM Awas Yojana Urban vs Rural) |
| 📄 **PDF Application Draft Generator** | Auto-generates a pre-filled application draft for any matched scheme, downloadable as a PDF |
| 🌐 **Multilingual Support** | The voice AI responds natively in whichever language the user speaks |

---

## 🧠 Tech Stack

### AI / ML
- **LLM**: `llama-3.3-70b-versatile` via [Groq](https://groq.com) (ultra-fast inference)
- **STT**: `whisper-large-v3` via Groq API
- **TTS**: [Cartesia](https://cartesia.ai) `sonic-multilingual` model
- **Embeddings**: `all-MiniLM-L6-v2` (sentence-transformers)
- **Vector Store**: [ChromaDB](https://www.trychroma.com/) — local, persistent

### Backend
- **Voice Infrastructure**: [LiveKit](https://livekit.io) (WebRTC rooms, agent SDK)
- **RAG Engine**: LangChain + ChromaDB
- **PDF Generation**: FPDF2

### Frontend
- **UI**: [Streamlit](https://streamlit.io) with custom CSS (glassmorphism, dark sidebar, micro-animations)

---

## 🏗️ Architecture

```
User Browser
    │
    ▼
Streamlit UI (policylens_ui.py)
    │
    ├── RAG Engine (rag_engine.py)
    │       └── ChromaDB (local vector DB, ~2500 policy docs)
    │               └── sentence-transformers embeddings
    │
    ├── Voice Agent (voice_agent.py)
    │       ├── LiveKit Room (WebRTC)
    │       ├── Groq Whisper STT
    │       ├── Groq LLaMA 3.3 LLM
    │       └── Cartesia TTS
    │
    └── PDF Generator (pdf_generator.py)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/DOCTOR-DOOM1/PolicyLens-AI.git
cd PolicyLens-AI
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
```bash
# Copy the example env file
copy .env.example .env   # Windows
cp .env.example .env     # macOS/Linux

# Edit .env and fill in your API keys
```

You'll need free accounts / API keys from:
- [Groq](https://console.groq.com) — for LLM + STT
- [LiveKit Cloud](https://livekit.io) — for voice rooms
- [Cartesia](https://cartesia.ai) — for TTS
- [ElevenLabs](https://elevenlabs.io) — (optional, fallback TTS)
- [OpenAI](https://platform.openai.com) — (optional, fallback LLM)

### 5. Build the Vector Database
```bash
# Ingest your PDF policy documents (place in /data folder first)
python ingest.py
```

### 6. Run the app
```bash
streamlit run policylens_ui.py
```

---

## 📁 Project Structure

```
PolicyLens-AI/
├── policylens_ui.py        # Main Streamlit UI (all pages)
├── rag_engine.py           # RAG pipeline: ChromaDB + LangChain
├── voice_agent.py          # LiveKit voice agent (STT + LLM + TTS)
├── pdf_generator.py        # PDF application draft generator
├── ingest.py               # PDF ingestion script for ChromaDB
├── ingest_json.py          # JSON data ingestion
├── ingest_massive_db.py    # Bulk ingestion for large datasets
├── inject_golden_data.py   # Injects curated scheme data
├── livekit_widget.html     # WebRTC voice widget (loaded in iframe)
├── app.py                  # Lightweight HF Spaces entry point
├── Dockerfile              # Docker config for cloud deployment
├── requirements.txt        # Python dependencies
├── .env.example            # API key template (copy to .env)
├── .streamlit/
│   └── config.toml         # Streamlit theme config
└── test_*.py               # Unit/integration test scripts
```

---

## 🎙️ Voice Agent Setup

The voice agent uses LiveKit for real-time WebRTC. To use it:

1. Create a free project at [LiveKit Cloud](https://cloud.livekit.io)
2. Add your `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` to `.env`
3. Launch the app, navigate to **AI Assistant**, and toggle **"Power On Backend Voice Agent"**

---

## 🌍 Supported Languages

The voice AI automatically detects and responds in:

| Language | Code |
|---|---|
| English | `en` |
| Hindi (हिन्दी) | `hi` |
| Marathi (मराठी) | `mr` |
| Tamil (தமிழ்) | `ta` |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) for blazing-fast LLM inference
- [LiveKit](https://livekit.io) for open-source WebRTC infrastructure
- [Cartesia](https://cartesia.ai) for multilingual neural TTS
- [ChromaDB](https://www.trychroma.com/) for the local vector store
- Indian Government policy portals for the source data

---

<p align="center">Built with ❤️ for the citizens of India</p>
