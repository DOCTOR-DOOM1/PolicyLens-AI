import os
import shutil
import tempfile
from huggingface_hub import HfApi

token = os.getenv("HF_TOKEN")
repo_id = "Doctor-Doom2/PolicyLens-AI"

api = HfApi()

# --- Step 1: Read secrets from .env (strip quotes cleanly) ---
print("Reading .env secrets...")
secrets = {}
with open(".env", "r") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            key = key.strip().strip('"').strip("'")
            val = val.strip().strip('"').strip("'")
            secrets[key] = val

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
            api.add_space_secret(repo_id=repo_id, key=key, value=secrets[key], token=token)
            print(f"  [OK] Set secret: {key}")
        except Exception as e:
            print(f"  [WARN] Could not set {key}: {e}")
    else:
        print(f"  [WARN] Key not found in .env: {key}")

# --- Step 2: (Disabled) Create app.py (HF Streamlit expects this as entry point) ---
# We no longer overwrite app.py because it contains custom code to download the database.

# --- Step 3: Upload only the necessary source files ---
FILES_TO_UPLOAD = [
    "app.py",
    "policylens_ui.py",
    "rag_engine.py",
    "voice_agent.py",
    "pdf_generator.py",
    "requirements.txt",
    "livekit_widget.html",
    ".streamlit/config.toml",
    "Dockerfile",
]

print("\nUploading core source files...")
for filepath in FILES_TO_UPLOAD:
    if os.path.exists(filepath):
        try:
            api.upload_file(
                path_or_fileobj=filepath,
                path_in_repo=filepath,
                repo_id=repo_id,
                repo_type="space",
                token=token,
            )
            print(f"  [OK] Uploaded: {filepath}")
        except Exception as e:
            print(f"  [WARN] Error uploading {filepath}: {e}")
    else:
        print(f"  [WARN] Skipping (not found): {filepath}")

# --- Step 4: (Disabled) Upload chroma_db using a staging temp folder ---
# The database is now kept in a Hugging Face Dataset repo instead to avoid Git LFS space issues.
print("\nSkipping chroma_db upload. The HF Space will download it from the Dataset repo.")

print("\nDeployment Complete!")
print(f"Visit: https://huggingface.co/spaces/{repo_id}")
