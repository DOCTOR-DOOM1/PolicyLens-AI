import os
from huggingface_hub import HfApi, create_repo, delete_repo

# Emergency Auth
TOKEN = os.getenv("HF_TOKEN")
api = HfApi(token=TOKEN)
REPO_ID = "Doctor-Doom2/PolicyLens-AI"

print("--- Step 1: Nuclear Deletion ---")
try:
    api.delete_repo(repo_id=REPO_ID, repo_type="space")
    print("Deleted successfully.")
except Exception as e:
    print(f"Delete skipped: {e}")

print("\n--- Step 2: Fresh Recreation (Static) ---")
try:
    api.create_repo(repo_id=REPO_ID, repo_type="space", space_sdk="static")
    print("Created successfully.")
except Exception as e:
    print(f"Creation failed: {e}")

print("\n--- Step 3: Minimal Metadata Push ---")
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
Emergency Recovery Build
"""
api.upload_file(
    path_or_fileobj=README.encode("utf-8"),
    path_in_repo="README.md",
    repo_id=REPO_ID,
    repo_type="space"
)

print("\n--- Step 4: Core Files Push ---")
BASE_DIR = r"C:\Users\Hp\Desktop\PolicyLens AI"
FILES = ["app.py", "policylens_ui.py", "rag_engine.py", "pdf_generator.py", "requirements.txt"]

for f in FILES:
    fpath = os.path.join(BASE_DIR, f)
    if os.path.exists(fpath):
        print(f"Uploading {f}...")
        api.upload_file(
            path_or_fileobj=fpath,
            path_in_repo=f,
            repo_id=REPO_ID,
            repo_type="space"
        )
    else:
        print(f"Skipping {f} (not found)")

print("\n--- DONE! CHECK YOUR SPACE NOW ---")
