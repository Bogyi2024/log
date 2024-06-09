import os
import re
import requests
import gdown
import subprocess

def fetch_links_from_pastebin(pastebin_link):
    response = requests.get(pastebin_link)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print(f"Error fetching from Pastebin: {response.status_code}")
        return []


def extract_google_drive_id(url):
    drive_id_pattern = re.compile(r'(?:drive.google.com/.*?id=|drive.google.com/file/d/|drive.google.com/open\?id=|drive.google.com/uc\?id=)([a-zA-Z0-9_-]{33,})')
    match = drive_id_pattern.search(url)
    if match:
        return match.group(1)
    else:
        print(f"Invalid Google Drive URL: {url}")
        return None

pastebin_link = "https://pastebin.com/raw/p2Xk0N0b"

single_line_batch_links = fetch_links_from_pastebin(pastebin_link)

if single_line_batch_links:
    output_path = "source/"
    os.makedirs(output_path, exist_ok=True)

    for url in single_line_batch_links:
        file_id = extract_google_drive_id(url)
        if file_id:
            try:
                subprocess.run(['gdown', file_id, '-O', output_path], check=True)
                print(f"Downloaded: {url}")
            except subprocess.CalledProcessError as e:
                print(f"Error downloading from Google Drive: {str(e)}")
        else:
            if url:
                filename = url.split('/')[-1]
                filepath = os.path.join(output_path, filename)
                try:
                    # Ensure aria2c is installed and in the system's PATH
                    os.system(f"aria2c.exe -x 16 -d {output_path} {url}")
                    print(f"Downloaded: {filename}")
                except Exception as e:
                    print(f"Error downloading {filename}: {str(e)}")
            else:
                print("Empty URL encountered")
else:
    print("No links found in the Pastebin link.")
  
