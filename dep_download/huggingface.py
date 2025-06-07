import os
import requests
from huggingface_hub import login, HfApi

# Step 1: Pastebin raw URL
pastebin_raw_url = "https://pastebin.com/raw/i39Dh6CM"

# Step 2: Fetch raw content
response = requests.get(pastebin_raw_url)
if response.status_code != 200:
    raise Exception("Failed to fetch Pastebin content")

# Step 3: Use the entire content as repo_name
repo_name = response.text.strip()
if not repo_name:
    raise ValueError("Pastebin content is empty. Expected a repo name.")

# Step 4: Hugging Face logic
write_token = "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"
login(write_token, add_to_git_credential=True)
api = HfApi()

user = api.whoami(write_token)
model_repo = f"{user['name']}/{repo_name}"

if not api.repo_exists(repo_id=model_repo):
    api.create_repo(repo_id=model_repo)
    print(f"Model Repo {model_repo} didn't exist, created!")
else:
    print(f"Model Repo {model_repo} exists, skipping creation.")

folder_path = "download"
commit_message = "Upload with Github"

if os.path.isdir(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            print(f"Uploading {file_name} to {model_repo}")
            api.upload_file(
                path_or_fileobj=file_path,
                path_in_repo=file_name,
                repo_id=model_repo,
                commit_message=commit_message,
            )
else:
    print("Invalid folder path. Please provide the correct folder path.")
