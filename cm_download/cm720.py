import os
import requests
import urllib.request

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
    output_path = "source/"
    os.makedirs(output_path, exist_ok=True)

    for url in single_line_batch_links:
        if url:
            filename = url.split('/')[-1]
            filepath = os.path.join(output_path, filename)
            try:
                urllib.request.urlretrieve(url, filepath)
                print(f"Downloaded: {filename}")
            except Exception as e:
                print(f"Error downloading {filename}: {str(e)}")
        else:
            print("Empty URL encountered")
