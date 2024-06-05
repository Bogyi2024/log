import os
from huggingface_hub import login, HfApi

# Authenticate with your write token
write_token = "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"
login(write_token, add_to_git_credential=True)

# Initialize Hugging Face API
api = HfApi()

# Define repository name
repo_name = "downloadx"

# Get user information
user = api.whoami(write_token)

# Define the model repo
model_repo = f"{user['name']}/{repo_name.strip()}"

# Create the model repo if it doesn't exist
if not api.repo_exists(repo_id=model_repo):
    api.create_repo(repo_id=model_repo)
    print(f"Model Repo {model_repo} didn't exist, created!")
else:
    print(f"Model Repo {model_repo} exists, skipping creation.")

# Define folder path containing files to upload
folder_path = "download"  # Assuming "download" directory is in the current directory
commit_message = "Upload with Google Colab"

# Upload files from the folder to the repository
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
