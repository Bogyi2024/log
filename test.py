import requests
import time

# ========== CONFIG ==========
token = "k1bfcv6qjuotf7nrohiia9gr6v"
file_id = "51144a58b67b5829bd4e5fa1eaa30b73"
api_url = f"https://rapidgator.net/api/v2/file/download?file_id={file_id}&token={token}"

# Optional proxy support (uncomment and fill in if needed)
# proxies = {
#     "http": "http://user:pass@ip:port",
#     "https": "http://user:pass@ip:port",
# }
proxies = None

# Browser-like headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

# ========== FUNCTION ==========
def get_download_url():
    for attempt in range(5):
        try:
            print(f"Attempt {attempt + 1}: contacting Rapidgator...")
            response = requests.get(api_url, headers=headers, timeout=30, proxies=proxies)

            if response.status_code != 200:
                print(f"HTTP Error: {response.status_code}")
                continue

            data = response.json()
            if data.get("status") == 200 and "download_url" in data:
                download_url = data["download_url"]
                delay = int(data.get("delay", 0))
                print(f"Success! Waiting {delay} seconds before showing the URL...")
                time.sleep(delay)
                print(f"\n🎯 Download URL: {download_url}")
                return download_url
            else:
                print(f"API response invalid: {data}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        time.sleep(2 ** attempt)  # exponential backoff

    print("❌ Failed to get the download URL after 5 attempts.")
    return None

# ========== RUN ==========
if __name__ == "__main__":
    get_download_url()
