from huggingface_hub import HfApi
import os
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

token = os.getenv("HF_TOKEN")
repo_id = "Doctor-Doom2/PolicyLens-Live"

api = HfApi(token=token)

print("Uploading local chroma_db directly to the Space to avoid runtime downloads...")

# Push entire folder directly to the space
api.upload_folder(
    folder_path="chroma_db",
    path_in_repo="chroma_db",
    repo_id=repo_id,
    repo_type="space",
    commit_message="Baking vector DB directly into the image for instant boot"
)

print("Upload successful!")

# Force restart to guarantee docker picks up the files
print("Restarting Space so Docker builds with the database pre-loaded...")
api.restart_space(repo_id=repo_id)

print("Done! The app will now boot instantly without getting stuck on downloading.")
