import os
import requests
import gdown
import subprocess
import re
import mediafire_dl



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

pastebin_link = "https://pastebin.com/raw/JK9NMvpc"

single_line_batch_links = fetch_links_from_pastebin(pastebin_link)

if single_line_batch_links:
    output_path = "source/"
    os.makedirs(output_path, exist_ok=True)

    for url in single_line_batch_links:
        file_id = extract_google_drive_id(url)
        if file_id:
            try:
                # Construct Google Drive file URL
                gdrive_url = f"https://drive.google.com/uc?id={file_id}"
                #os.chdir(output_path)
                output_file = os.path.join(output_path, f"{file_id}.file")
                # Download the file with gdown to the source folder
                gdown.download(gdrive_url, output=output_file, quiet=False)
                #os.chdir("./")
                
                print(f"Downloaded: {gdrive_url}")
            except Exception as e:
                print(f"Error downloading from Google Drive: {str(e)}")
        else:
            if url:
                if url.startswith("https://download") or "mediafire.com" in url:
                    try:
                        os.chdir(output_path)
                        if url.startswith("https://download"):
                            # Modify the URL to the Mediafire format
                            url_parts = url.split("/")
                            new_url = f"https://www.mediafire.com/file/{url_parts[-2]}/{url_parts[-1]}"
                            mediafire_dl.download(new_url, quiet=False)
                        else:
                            mediafire_dl.download(url, quiet=False)
                        os.chdir("./")
                        print(f"Downloaded: {url}")
                    except Exception as e:
                        print(f"Error downloading from Mediafire: {str(e)}")
                else:
                    filename = url.split('/')[-1]
                    filepath = os.path.join(output_path, filename)
                    try:
                        # Ensure aria2c is installed and in the system's PATH
                        subprocess.run(['aria2c', '-x', '16', '-d', output_path, url], check=True)
                        print(f"Downloaded: {filename}")
                    except Exception as e:
                        print(f"Error downloading {filename}: {str(e)}")
            else:
                print("Empty URL encountered")
else:
    print("No links found in the Pastebin link.")
