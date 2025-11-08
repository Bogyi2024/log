import os
import gdown
import subprocess
import re
import mediafire_dl

# Note: 'requests' is no longer needed for getting the links list

def extract_google_drive_id(url):
    drive_id_pattern = re.compile(r'(?:drive.google.com/.*?id=|drive.google.com/file/d/|drive.google.com/open\?id=|drive.google.com/uc\?id=)([a-zA-Z0-9_-]{33,})')
    match = drive_id_pattern.search(url)
    if match:
        return match.group(1)
    else:
        print(f"Invalid Google Drive URL: {url}")
        return None

# --- THIS IS THE MODIFIED SECTION ---
# Get the raw list of links from the environment variable
# This variable comes from the "Links List" tab in your GUI
links_content = os.getenv('LINKS_CONTENT')

if links_content:
    # Split the raw text into a list of URLs
    single_line_batch_links = links_content.splitlines()
    print(f"Loaded {len(single_line_batch_links)} links from environment variable.")
else:
    print("Error: LINKS_CONTENT environment variable not found or is empty.")
    single_line_batch_links = []
# --- END OF MODIFIED SECTION ---


if single_line_batch_links:
    output_path = "source/"
    os.makedirs(output_path, exist_ok=True)

    for url in single_line_batch_links:
        if not url.strip(): # Skip empty lines
            continue
            
        file_id = extract_google_drive_id(url)
        if file_id:
            try:
                # Construct Google Drive file URL
                gdrive_url = f"https://drive.google.com/uc?id={file_id}"
                output_file = os.path.join(output_path, f"{file_id}.file")
                # Download the file with gdown to the source folder
                gdown.download(gdrive_url, output=output_file, quiet=False)
                print(f"Downloaded: {gdrive_url}")
            except Exception as e:
                print(f"Error downloading from Google Drive: {str(e)}")
        else:
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
                    os.chdir("../") # Go back up from 'source'
                    print(f"Downloaded: {url}")
                except Exception as e:
                    print(f"Error downloading from Mediafire: {str(e)}")
                    os.chdir("../") # Ensure we go back up even on error
            else:
                filename = url.split('/')[-1]
                filepath = os.path.join(output_path, filename)
                try:
                    # Ensure aria2c is available (downloaded in .bat)
                    # We call './aria2c' because it's in the current folder
                    subprocess.run(['./aria2c', '-x', '16', '-d', output_path, url], check=True)
                    print(f"Downloaded: {filename}")
                except Exception as e:
                    print(f"Error downloading {filename}: {str(e)}")
else:
    print("No links found in the links content.")
