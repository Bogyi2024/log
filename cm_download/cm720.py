import os
import requests
import gdown

def fetch_links_from_pastebin(pastebin_link):
    response = requests.get(pastebin_link)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print(f"Error fetching from Pastebin: {response.status_code}")
        return []

pastebin_link = "https://pastebin.com/raw/p2Xk0N0b"

single_line_batch_links = fetch_links_from_pastebin(pastebin_link)

if single_line_batch_links:
    output_path = "source/"
    os.makedirs(output_path, exist_ok=True)

    for url in single_line_batch_links:
        if "drive.google.com" in url:
            try:
                gdown.download(url=url, output=output_path, fuzzy=True)
                print(f"Downloaded: {url}")
            except Exception as e:
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
