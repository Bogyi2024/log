import requests
import re

url = "" # @param {type:"string"}

response = requests.get(url)

if response.status_code == 200:
    content = response.text
    links = re.findall(r'href=[\'"]?([^\'" >]+)', content)

    for link in links:
        if link.startswith('http'):
            output_path = "" # @param {type:"string"}
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
                final_url= f"https://{domain}/api/file/direct_link?key={apiKey}&file_code={filecodex}"
                response = requests.get(final_url)

                if response.status_code == 200:
                    json_data = response.json()
                    download_url = json_data.get('result', {}).get('url')
                    !wget -P $output_path $download_url
                else:
                    print("Error while fetching Katfile API")
            else:
                print("Error while fetching Katfile API")
else:
    print("Error while fetching URL:", response.status_code)
