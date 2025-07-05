import requests
import time

# Your Rapidgator API link
token = "k1bfcv6qjuotf7nrohiia9gr6v"
id = "51144a58b67b5829bd4e5fa1eaa30b73"
api_url = f'https://rapidgator.net/api/v2/file/download?file_id={id}&token={token}'

# Step 1: Send the request to the API
response = requests.get(api_url)

# Step 2: Check if response is OK and parse JSON
if response.status_code == 200:
    data = response.json()
    
    if data.get("status") == 200 and "download_url" in data:
        download_url = data["download_url"]
        delay = int(data.get("delay", 0))

        print(f"Waiting {delay} seconds before download...")
        time.sleep(delay)

        print(f"Direct Download URL: {download_url}")

        # Optional: download the file
        # Uncomment below to save it
        '''
        filename = download_url.split('/')[-1]
        file_response = requests.get(download_url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in file_response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File saved as: {filename}")
        '''
    else:
        print(f"Failed: {data}")
else:
    print(f"HTTP Error: {response.status_code}")
