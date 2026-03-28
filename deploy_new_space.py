"""
Script to deploy the app to a fresh Hugging Face Space with a NEW NAME
to bypass the "expected object, received undefined" corrupted metadata error.
"""
import os
import sys
import time
from pathlib import Path

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    from huggingface_hub import HfApi, create_repo, delete_repo
except ImportError:
    os.system(f"{sys.executable} -m pip install huggingface_hub -q")
    from huggingface_hub import HfApi, create_repo, delete_repo

from dotenv import load_dotenv
load_dotenv()

HF_TOKEN    = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    HF_TOKEN = os.getenv("HF_TOKEN")

SPACE_OWNER = "Doctor-Doom2"
SPACE_NAME  = "PolicyLens-App"  # NEW NAME
SPACE_ID    = f"{SPACE_OWNER}/{SPACE_NAME}"
SPACE_DIR   = Path(__file__).parent / "hf_space_tmp"

api = HfApi(token=HF_TOKEN)

# ── Delete corrupted space if it still exists
try:
    delete_repo(repo_id=f"{SPACE_OWNER}/PolicyLens-AI", repo_type="space", token=HF_TOKEN)
    print("Deleted old corrupted Space: PolicyLens-AI")
except Exception:
    pass

# ── STEP 1: Create fresh Space with sdk: streamlit
print(f"\nCreating fresh Space: {SPACE_ID} (sdk=streamlit) ...")
create_repo(
    repo_id=SPACE_ID,
    repo_type="space",
    space_sdk="docker",
    token=HF_TOKEN,
    private=False,
    exist_ok=True,
)
print("   Space created OK.")
time.sleep(3)

# ── STEP 2: Upload README.md (must be exact)
README_CONTENT = """\
---
title: PolicyLens App
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
short_description: AI-powered government policy eligibility checker for India
---

# PolicyLens AI

An intelligent RAG-based assistant helping citizens discover government schemes.
Built with LangChain, ChromaDB, Groq LLM, and Streamlit.
"""

print("\nUploading README.md ...")
api.upload_file(
    path_or_fileobj=README_CONTENT.encode("utf-8"),
    path_in_repo="README.md",
    repo_id=SPACE_ID,
    repo_type="space",
    token=HF_TOKEN,
)

# ── STEP 3: Upload requirements.txt
REQUIREMENTS = """\
--extra-index-url https://download.pytorch.org/whl/cpu
langchain==0.3.19
langchain-community==0.3.18
langchain-groq==0.3.2
langchain-huggingface==0.1.2
chromadb==0.6.3
pypdf==5.4.0
python-dotenv==1.0.1
streamlit==1.44.0
aiohttp==3.11.14
fpdf2==2.8.3
sentence-transformers==3.4.1
huggingface_hub>=0.22.0
"""

print("Uploading requirements.txt ...")
api.upload_file(
    path_or_fileobj=REQUIREMENTS.encode("utf-8"),
    path_in_repo="requirements.txt",
    repo_id=SPACE_ID,
    repo_type="space",
    token=HF_TOKEN,
)

# ── STEP 4: Upload .streamlit/config.toml
STREAMLIT_CONFIG = """\
[server]
headless = true
port = 7860
enableCORS = false
enableXsrfProtection = false

[theme]
base = "light"
"""

print("Uploading .streamlit/config.toml ...")
api.upload_file(
    path_or_fileobj=STREAMLIT_CONFIG.encode("utf-8"),
    path_in_repo=".streamlit/config.toml",
    repo_id=SPACE_ID,
    repo_type="space",
    token=HF_TOKEN,
)

# ── STEP 5: Upload all app Python/HTML files
UPLOAD_FILES = [
    "app.py",
    "policylens_ui.py",
    "rag_engine.py",
    "voice_agent.py",
    "pdf_generator.py",
    "livekit_widget.html",
    "Dockerfile",
]

# We need to grab them from where they are currently, either current dir or hf_space_tmp
# the current directory has the valid verified files so let's use current dir.
CURRENT_DIR = Path(__file__).parent

print("\nUploading app files ...")
for filename in UPLOAD_FILES:
    filepath = CURRENT_DIR / filename
    if not filepath.exists():
        print(f"   SKIP: {filename} (not found in {CURRENT_DIR})")
        continue
    size_kb = filepath.stat().st_size // 1024
    print(f"   Uploading: {filename} ({size_kb} KB)")
    api.upload_file(
        path_or_fileobj=str(filepath),
        path_in_repo=filename,
        repo_id=SPACE_ID,
        repo_type="space",
        token=HF_TOKEN,
    )
    print(f"   OK: {filename}")

print(f"""
=== DONE ===
Space deployed at NEW URL: https://huggingface.co/spaces/{SPACE_ID}

HF is now installing requirements and starting Streamlit.
Watch logs at: https://huggingface.co/spaces/{SPACE_ID}/logs

IMPORTANT - Remember to set your GROQ_API_KEY in Space Settings!
""")
