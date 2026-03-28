import huggingface_hub

api = huggingface_hub.HfApi()
repo_id = "Doctor-Doom2/PolicyLens-AI"
token = os.getenv("HF_TOKEN")

readme_content = """---
title: PolicyLens AI
emoji: 🚀
colorFrom: red
colorTo: red
sdk: streamlit
app_file: app.py
pinned: false
---
"""

print("Updating README.md to use Streamlit SDK...")
api.upload_file(
    path_or_fileobj=readme_content.encode("utf-8"),
    path_in_repo="README.md",
    repo_id=repo_id,
    repo_type="space",
    token=token
)

print("Deleting Dockerfile (no longer needed)...")
try:
    api.delete_file("Dockerfile", repo_id=repo_id, repo_type="space", token=token)
except Exception as e:
    print("Dockerfile already deleted or not found.")

print("Space configuration updated!")
