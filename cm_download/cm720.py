import os
import requests

def fetch_links_from_pastebin(pastebin_link):
    response = requests.get(pastebin_link)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print(f"Error fetching from Pastebin: {response.status_code}")
        return []

pastebin_link = "https://pastebin.com/p2Xk0N0b"
#pastebin_link = "https://raw.githubusercontent.com/Bogyi2024/log/main/dep_download/url.txt"

single_line_batch_links = fetch_links_from_pastebin(pastebin_link)

if single_line_batch_links:
    output_path = "source/"
    os.makedirs(output_path, exist_ok=True)

    for url in single_line_batch_links:
        if url:
            filename = url.split('/')[-1]
            filepath = os.path.join(output_path, filename)
            try:
                os.system(f"aria2c.exe -x 16 -d {output_path} {url}")
                print(f"Downloaded: {filename}")
            except Exception as e:
                print(f"Error downloading {filename}: {str(e)}")
        else:
            print("Empty URL encountered")
