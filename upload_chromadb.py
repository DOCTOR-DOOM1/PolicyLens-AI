import os
from huggingface_hub import HfApi, login

login(token=os.getenv("HF_TOKEN"))
api = HfApi()
dataset_repo = "Doctor-Doom2/policylens-chromadb"

# Upload each file individually to avoid memory issues
for root, dirs, files in os.walk("chroma_db"):
    for fname in files:
        fpath = os.path.join(root, fname)
        # path relative to chroma_db parent
        repo_path = fpath.replace("\\", "/")
        size_mb = os.path.getsize(fpath) / 1024 / 1024
        print(f"Uploading {repo_path} ({size_mb:.1f} MB)...")
        try:
            api.upload_file(
                path_or_fileobj=fpath,
                path_in_repo=repo_path,
                repo_id=dataset_repo,
                repo_type="dataset",
            )
            print(f"  [OK] {repo_path}")
        except Exception as e:
            print(f"  [ERR] {repo_path}: {e}")

print("\nAll chroma_db files uploaded to Dataset repo!")
print(f"Dataset URL: https://huggingface.co/datasets/{dataset_repo}")
