import os
import sys
import time
from pathlib import Path

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    from huggingface_hub import HfApi, create_repo
except ImportError:
    os.system(f"{sys.executable} -m pip install huggingface_hub -q")
    from huggingface_hub import HfApi, create_repo

from dotenv import load_dotenv
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

SPACE_OWNER = "Doctor-Doom2"
SPACE_NAME  = "PolicyLens-Voice-Native"
SPACE_ID    = f"{SPACE_OWNER}/{SPACE_NAME}"
CURRENT_DIR = Path(__file__).parent

api = HfApi(token=HF_TOKEN)

print(f"\n🚀 Creating Voice Backend Space: {SPACE_ID} (sdk=gradio) [DOCKER BYPASS] ...")
create_repo(
    repo_id=SPACE_ID,
    repo_type="space",
    space_sdk="gradio",
    token=HF_TOKEN,
    private=False,
    exist_ok=True,
)
print("✅ Space created OK.")
time.sleep(2)

README_CONTENT = f"""\
---
title: PolicyLens Voice Native
emoji: 🎙️
colorFrom: green
colorTo: blue
sdk: gradio
app_port: 7860
pinned: false
---

# PolicyLens Voice Backend (LiveKit)
"""

print("\nUploading README.md ...")
api.upload_file(
    path_or_fileobj=README_CONTENT.encode("utf-8"),
    path_in_repo="README.md",
    repo_id=SPACE_ID,
    repo_type="space",
    token=HF_TOKEN,
)

REQUIREMENTS = """\
--extra-index-url https://download.pytorch.org/whl/cpu
livekit>=0.20.0
livekit-api>=1.0.2
livekit-agents>=1.0.21
livekit-plugins-openai>=1.5.0
livekit-plugins-cartesia>=1.5.1
livekit-plugins-silero>=1.5.0
python-dotenv==1.0.1
"""

print("Uploading requirements.txt ...")
api.upload_file(
    path_or_fileobj=REQUIREMENTS.encode("utf-8"),
    path_in_repo="requirements.txt",
    repo_id=SPACE_ID,
    repo_type="space",
    token=HF_TOKEN,
)

print("\nUploading voice_agent.py as app.py ...")
with open(CURRENT_DIR / "voice_agent.py", "rb") as f:
    voice_agent_content = f.read()

# For HF Gradio natively, the file MUST be named app.py
api.upload_file(
    path_or_fileobj=voice_agent_content,
    path_in_repo="app.py",
    repo_id=SPACE_ID,
    repo_type="space",
    token=HF_TOKEN,
)

print(f"""
=== 🎉 NATIVE DEPLOYMENT COMPLETE ===
Your dedicated native Python backend has been deployed at: 
https://huggingface.co/spaces/{SPACE_ID}
""")
