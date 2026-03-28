import os
from huggingface_hub import HfApi, create_repo

# Emergency Auth
TOKEN = os.getenv("HF_TOKEN")
api = HfApi(token=TOKEN)
REPO_ID = "Doctor-Doom2/PolicyLens-AI"

print("--- Step 1: Force Recreation ---")
try:
    create_repo(repo_id=REPO_ID, repo_type="space", space_sdk="static", token=TOKEN, exist_ok=True)
    print("Created/Verified successfully.")
except Exception as e:
    print(f"Recreation failed: {e}")

print("\n--- Step 2: Minimal Metadata Push (ASCII) ---")
README = """---
title: PolicyLens AI
emoji: 🔎
colorFrom: blue
colorTo: purple
sdk: streamlit
app_file: app.py
pinned: false
---

# PolicyLens AI
RAG assistant for government schemes.
"""
api.upload_file(
    path_or_fileobj=README.encode("utf-8"),
    path_in_repo="README.md",
    repo_id=REPO_ID,
    repo_type="space"
)

print("\n--- Step 3: Core Files Upload ---")
BASE_DIR = r"C:\Users\Hp\Desktop\PolicyLens AI"
FILES = ["app.py", "policylens_ui.py", "rag_engine.py", "pdf_generator.py", "requirements.txt", "livekit_widget.html"]

for f in FILES:
    fpath = os.path.join(BASE_DIR, f)
    if os.path.exists(fpath):
        print(f"Uploading {f}...")
        try:
            api.upload_file(
                path_or_fileobj=fpath,
                path_in_repo=f,
                repo_id=REPO_ID,
                repo_type="space"
            )
            print(f"   Done: {f}")
        except Exception as e:
            print(f"   Failed {f}: {e}")
    else:
        print(f"Skipping {f} (not found)")

# Also upload .streamlit/config.toml
ST_CONFIG_PATH = os.path.join(BASE_DIR, ".streamlit", "config.toml")
if os.path.exists(ST_CONFIG_PATH):
    print("Uploading Streamlit config...")
    api.upload_file(
        path_or_fileobj=ST_CONFIG_PATH,
        path_in_repo=".streamlit/config.toml",
        repo_id=REPO_ID,
        repo_type="space"
    )

print("\n--- DONE! CHECK YOUR SPACE NOW ---")
