import os
import sys
import subprocess
import requests
import re
from urllib.parse import unquote, urlparse
from huggingface_hub import HfApi

# --- Configuration ---
LINK = os.environ.get("LINK")
TOOL = os.environ.get("TOOL", "aria2c")
HF_REPO = os.environ.get("HF_REPO")
HF_TYPE = os.environ.get("HF_TYPE", "model")
HF_TOKEN = os.environ.get("HF_TOKEN")

if not LINK or not HF_REPO or not HF_TOKEN:
    print("Error: Missing required environment variables.")
    sys.exit(1)

def get_filename_from_url(url, response=None):
    """Attempts to determine filename from Content-Disposition header or URL path."""
    filename = None
    
    # 1. Try Content-Disposition if response is provided
    if response and "Content-Disposition" in response.headers:
        cd = response.headers["Content-Disposition"]
        fname_match = re.findall(r'filename\*?=([^;]+)', cd)
        if fname_match:
            filename = fname_match[0].strip().strip('"').strip("'")
    
    # 2. Try URL path
    if not filename:
        parsed = urlparse(url)
        path = unquote(parsed.path)
        filename = os.path.basename(path)
    
    # 3. Fallback
    if not filename or filename == "":
        filename = "downloaded_file.dat"
        
    return filename

def download_smartdl(url):
    """Python-based downloader with progress bar (requests)."""
    print(f"Starting SmartDL (Python Requests) for: {url}")
    
    # Stream to get headers first
    with requests.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        filename = get_filename_from_url(url, r)
        print(f"Target Filename: {filename}")
        
        with open(filename, 'wb') as f:
            total_length = r.headers.get('content-length')
            if total_length is None: # no content length header
                f.write(r.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in r.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl//1024}KB")
                    sys.stdout.flush()
    print("\nDownload complete.")
    return filename

def download_aria2c(url):
    print(f"Starting aria2c for: {url}")
    # aria2c automatically handles filenames usually, but let's force a check if needed
    # We use -x 16 for max connections
    cmd = ["aria2c", "-x", "16", "-s", "16", "--console-log-level=warn", url]
    subprocess.run(cmd, check=True)
    # Aria2c saves to current dir. We need to find the file.
    # Simple heuristic: find the newest file
    return max([f for f in os.listdir(".") if os.path.isfile(f)], key=os.path.getctime)

def download_wget(url):
    print(f"Starting wget for: {url}")
    cmd = ["wget", "--content-disposition", url]
    subprocess.run(cmd, check=True)
    return max([f for f in os.listdir(".") if os.path.isfile(f)], key=os.path.getctime)

def download_curl(url):
    print(f"Starting curl for: {url}")
    # Curl needs -O to save with remote name, or -J to use content-disposition
    cmd = ["curl", "-L", "-O", "-J", url]
    subprocess.run(cmd, check=True)
    return max([f for f in os.listdir(".") if os.path.isfile(f)], key=os.path.getctime)

def main():
    print(f"--- Processing Link: {LINK} ---")
    print(f"--- Tool: {TOOL} ---")

    filename = None
    
    try:
        if TOOL == "smartdl":
            filename = download_smartdl(LINK)
        elif TOOL == "aria2c":
            filename = download_aria2c(LINK)
        elif TOOL == "wget":
            filename = download_wget(LINK)
        elif TOOL == "curl":
            filename = download_curl(LINK)
        else:
            print(f"Unknown tool {TOOL}, defaulting to aria2c")
            filename = download_aria2c(LINK)
            
        print(f"Successfully downloaded: {filename}")
        
        print(f"--- Uploading to HuggingFace ({HF_REPO}) ---")
        api = HfApi(token=HF_TOKEN)
        
        # Determine path in repo (root)
        path_in_repo = filename
        
        api.upload_file(
            path_or_fileobj=filename,
            path_in_repo=path_in_repo,
            repo_id=HF_REPO,
            repo_type=HF_TYPE
        )
        print("Upload Complete!")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
