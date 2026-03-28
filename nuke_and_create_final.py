from huggingface_hub import HfApi, CommitOperationAdd, create_repo, delete_repo
import os
import time
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("HF_TOKEN")
repo_id = "Doctor-Doom2/PolicyLens-Live"

api = HfApi(token=token)

print(f"Creating fresh Space: {repo_id}...")
create_repo(
    repo_id=repo_id,
    repo_type="space",
    space_sdk="docker",
    token=token,
    private=False,
    exist_ok=True
)

time.sleep(3) # Wait for backend metadata sync

UPLOAD_FILES = [
    "app.py",
    "policylens_ui.py",
    "rag_engine.py",
    "voice_agent.py",
    "pdf_generator.py",
    "livekit_widget.html",
    "Dockerfile",
    "requirements.txt",
    ".streamlit/config.toml"
]

README_CONTENT = """\
---
title: PolicyLens Live
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---
"""

operations = []
operations.append(CommitOperationAdd(path_in_repo="README.md", path_or_fileobj=README_CONTENT.encode("utf-8")))

for f in UPLOAD_FILES:
    if os.path.exists(f):
        operations.append(CommitOperationAdd(path_in_repo=f, path_or_fileobj=f))

print(f"Committing {len(operations)} files atomically...")
api.create_commit(
    repo_id=repo_id,
    repo_type="space",
    operations=operations,
    commit_message="Initial commit"
)

print("Pushing secrets...")
secrets = {
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    "LIVEKIT_URL": os.getenv("LIVEKIT_URL"),
    "LIVEKIT_API_KEY": os.getenv("LIVEKIT_API_KEY"),
    "LIVEKIT_API_SECRET": os.getenv("LIVEKIT_API_SECRET"),
    "CARTESIA_API_KEY": os.getenv("CARTESIA_API_KEY"),
}

for k, v in secrets.items():
    if v:
        api.add_space_secret(repo_id=repo_id, key=k, value=v)

print(f"ALL DONE! New Space URL: https://huggingface.co/spaces/{repo_id}")
