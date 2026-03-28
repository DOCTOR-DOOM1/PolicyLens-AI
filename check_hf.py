import requests
url = 'https://huggingface.co/spaces/Doctor-Doom2/PolicyLens-AI/raw/main/README.md'
headers = {'Authorization': f'Bearer {os.getenv("HF_TOKEN")}'}
r = requests.get(url, headers=headers)
with open('tmp_readme.txt', 'wb') as f:
    f.write(r.content)
