"""
Nuclear option: Delete the broken HF Space and recreate it from scratch.
Uses huggingface_hub API directly - no git, no Docker issues.
Uses sdk: streamlit (HF manages the runtime, no Dockerfile needed).
"""
import os
import sys
import time
from pathlib import Path

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    from huggingface_hub import HfApi, create_repo, delete_repo
    from huggingface_hub.utils import RepositoryNotFoundError
except ImportError:
    print("Installing huggingface_hub...")
    os.system(f"{sys.executable} -m pip install huggingface_hub -q")
    from huggingface_hub import HfApi, create_repo, delete_repo
    from huggingface_hub.utils import RepositoryNotFoundError

from dotenv import load_dotenv
load_dotenv()

# ── CONFIG ──────────────────────────────────────────────────────────────────
HF_TOKEN    = os.getenv("HF_TOKEN")  # from .env if set
SPACE_OWNER = "Doctor-Doom2"
SPACE_NAME  = "PolicyLens-AI"
SPACE_ID    = f"{SPACE_OWNER}/{SPACE_NAME}"
SPACE_DIR   = Path(__file__).parent / "hf_space_tmp"

# ── Get token ───────────────────────────────────────────────────────────
if not HF_TOKEN:
    HF_TOKEN = os.getenv("HF_TOKEN")
    print(f"Using provided HF token for account: Doctor-Doom2")

api = HfApi(token=HF_TOKEN)

# ── STEP 1: Delete the broken Space ─────────────────────────────────────────
print(f"\nDeleting broken Space: {SPACE_ID} ...")
try:
    delete_repo(repo_id=SPACE_ID, repo_type="space", token=HF_TOKEN)
    print("   Space deleted OK.")
except RepositoryNotFoundError:
    print("   Space not found (already deleted).")
except Exception as e:
    print(f"   Delete warning: {e} - continuing...")

time.sleep(4)

# ── STEP 2: Create fresh Space with sdk: streamlit ──────────────────────────
print(f"\nCreating fresh Space: {SPACE_ID} (sdk=streamlit) ...")
create_repo(
    repo_id=SPACE_ID,
    repo_type="space",
    space_sdk="streamlit",
    token=HF_TOKEN,
    private=False,
    exist_ok=True,
)
print("   Space created OK.")
time.sleep(3)

# ── STEP 3: Upload README.md ─────────────────────────────────────────────────
README_CONTENT = """\
---
title: PolicyLens AI
emoji: \U0001f50d
colorFrom: blue
colorTo: purple
sdk: streamlit
app_file: app.py
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

# ── STEP 4: Upload requirements.txt ─────────────────────────────────────────
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

# ── STEP 5: Upload .streamlit/config.toml ────────────────────────────────────
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

# ── STEP 6: Upload all app Python/HTML files ──────────────────────────────────
UPLOAD_FILES = [
    "app.py",
    "policylens_ui.py",
    "rag_engine.py",
    "pdf_generator.py",
    "livekit_widget.html",
]

print("\nUploading app files ...")
for filename in UPLOAD_FILES:
    filepath = SPACE_DIR / filename
    if not filepath.exists():
        print(f"   SKIP: {filename} (not found in {SPACE_DIR})")
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
Space recreated: https://huggingface.co/spaces/{SPACE_ID}

HF is now installing requirements and starting Streamlit.
First build takes ~5-8 min. Watch logs at:
https://huggingface.co/spaces/{SPACE_ID}/logs

IMPORTANT - Set these secrets in Space Settings > Variables and secrets:
  GROQ_API_KEY = your_groq_key
  HF_TOKEN     = your_hf_token  (for ChromaDB dataset download)
""")
