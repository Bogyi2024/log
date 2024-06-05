import requests
import re
import os

url = "https://pastebin.com/raw/wfBkJJpS"  # URL containing links to download
output_path = "download/"  # Output path for downloaded files

response = requests.get(url)

if response.status_code == 200:
    content = response.text
    links = re.findall(r'href=[\'"]?([^\'" >]+)', content)

    for link in links:
        if link.startswith('http'):
            apiKey = "699996yph6h88a7rc6c1g8"
            parts = link.split('/')
            domain = parts[2]
            filecode = parts[3]

            cloneurl = f"https://{domain}/api/file/clone?key={apiKey}&file_code={filecode}"
            response = requests.get(cloneurl)

            if response.status_code == 200:
                json_data = response.json()
                download_url = json_data.get('result', {}).get('url')

                parts_final = download_url.split('/')
                filecodex = parts_final[3]
                final_url = f"https://{domain}/api/file/direct_link?key={apiKey}&file_code={filecodex}"
                response = requests.get(final_url)

                if response.status_code == 200:
                    json_data = response.json()
                    download_url = json_data.get('result', {}).get('url')

                    # Create the output directory if it doesn't exist
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)

                    # Extract filename from URL and download the file to the output path
                    filename = download_url.split('/')[-1]
                    filepath = os.path.join(output_path, filename)
                    with open(filepath, 'wb') as f:
                        f.write(requests.get(download_url).content)
                else:
                    print("Error while fetching Katfile direct link API")
            else:
                print("Error while fetching Katfile clone API")
else:
    print("Error while fetching URL:", response.status_code)
