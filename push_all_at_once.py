from huggingface_hub import HfApi, CommitOperationAdd
import os

token = os.getenv("HF_TOKEN")
repo_id = "Doctor-Doom2/PolicyLens-App"

api = HfApi(token=token)

# Files to commit
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

# Create a single unified commit
operations = []
operations.append(CommitOperationAdd(path_in_repo="README.md", path_or_fileobj=README_CONTENT.encode("utf-8")))

for f in UPLOAD_FILES:
    if os.path.exists(f):
        operations.append(CommitOperationAdd(path_in_repo=f, path_or_fileobj=f))

print(f"Pushing {len(operations)} files in ONE atomic commit...")
api.create_commit(
    repo_id=repo_id,
    repo_type="space",
    operations=operations,
    commit_message="Atomic deploy to fix build logs issue"
)

# Restart the space to guarantee it picks up the atomic commit cleanly
print("Restarting space...")
api.restart_space(repo_id=repo_id)

print("Done. Check logs now!")
