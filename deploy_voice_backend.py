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

# We check multiple sources for the HF Token
HF_TOKEN = os.getenv("HF_TOKEN") or input("Enter your Hugging Face Token (starts with hf_...): ")

SPACE_OWNER = "Doctor-Doom2"
SPACE_NAME  = "PolicyLens-Voice-Backend"
SPACE_ID    = f"{SPACE_OWNER}/{SPACE_NAME}"
CURRENT_DIR = Path(__file__).parent

api = HfApi(token=HF_TOKEN)

print(f"\n🚀 Creating Voice Backend Space: {SPACE_ID} (sdk=docker) ...")
create_repo(
    repo_id=SPACE_ID,
    repo_type="space",
    space_sdk="docker",
    token=HF_TOKEN,
    private=False,
    exist_ok=True,
)
print("✅ Space created OK.")
time.sleep(2)

README_CONTENT = f"""\
---
title: PolicyLens Voice Backend
emoji: 🎙️
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# PolicyLens Voice Backend (LiveKit)

This is a headless worker space handling secure, permanent audio connections for the PolicyLens AI project.
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

DOCKERFILE = """\
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY voice_agent.py .

EXPOSE 7860
# This runs the dummy port 7860 server inside voice_agent AND the LiveKit CLI natively.
CMD ["python", "voice_agent.py", "start"]
"""

print("Uploading Dockerfile ...")
api.upload_file(
    path_or_fileobj=DOCKERFILE.encode("utf-8"),
    path_in_repo="Dockerfile",
    repo_id=SPACE_ID,
    repo_type="space",
    token=HF_TOKEN,
)

print("\nUploading voice_agent.py ...")
api.upload_file(
    path_or_fileobj=str(CURRENT_DIR / "voice_agent.py"),
    path_in_repo="voice_agent.py",
    repo_id=SPACE_ID,
    repo_type="space",
    token=HF_TOKEN,
)

# Upload Secrets
print("\nReading .env secrets...")
secrets = {}
env_path = CURRENT_DIR / ".env"
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                secrets[k.strip().strip('"').strip("'")] = v.strip().strip('"').strip("'")

SECRETS_TO_UPLOAD = [
    "GROQ_API_KEY",
    "LIVEKIT_URL",
    "LIVEKIT_API_KEY",
    "LIVEKIT_API_SECRET",
    "CARTESIA_API_KEY",
]

print("Setting secrets on Hugging Face Space...")
for key in SECRETS_TO_UPLOAD:
    if key in secrets:
        try:
            api.add_space_secret(repo_id=SPACE_ID, key=key, value=secrets[key])
            print(f"  [OK] Set secret: {key}")
        except Exception as e:
            print(f"  [WARN] Could not set {key}: {e}")
    else:
        print(f"  [WARN] Key not found in .env: {key}")

print(f"""
=== 🎉 DEPLOYMENT COMPLETE ===
Your dedicated backend has been deployed at: 
https://huggingface.co/spaces/{SPACE_ID}

Secrets have been securely uploaded. Hugging Face will now build and start the backend!
""")
