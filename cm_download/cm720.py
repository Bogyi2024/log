import os
import requests
import subprocess

# Function to fetch links from Pastebin
def fetch_links_from_pastebin(pastebin_link):
    response = requests.get(pastebin_link)
    if response.status_code == 200:
        return response.text.strip().split('\n')
    else:
        print("Error fetching links from Pastebin")
        return []

pastebin_link = "https://pastebin.com/raw/0gUFE5Q0"
single_line_batch_links = fetch_links_from_pastebin(pastebin_link)

if single_line_batch_links:
    output_path = "download/"
    os.makedirs(output_path, exist_ok=True)

    for url in single_line_batch_links:
        if url:
            response = requests.get(url)  # Send a request to the URL
            if response.status_code == 200:
                download_url = response.url
                # Construct the command for curl
                local_filename = os.path.join(output_path, download_url.split('/')[-1])
                command = ['curl', '-o', local_filename, download_url]
                subprocess.run(command, check=True)
                print(f"Downloaded: {local_filename}")
            else:
                print(f"Error fetching URL: {url}")
        else:
            print("Empty URL encountered")
