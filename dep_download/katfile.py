# @title <img src="https://assets.katfile.com/images/logo.png" width="100px">

import os, re, requests

single_line_batch_links = "" # @param {type:"string"}

perlink = single_line_batch_links.split(" ")

if single_line_batch_links != "" :

    files = perlink

#else:

#    file_url1 = "" # @param {type:"string"}
#    file_url2 = "" # @param {type:"string"}
#    file_url3 = "" # @param {type:"string"}
#    file_url4 = "" # @param {type:"string"}
#    file_url5 = "" # @param {type:"string"}
#
#
#    files = [file_url1, file_url2, file_url3, file_url4, file_url5]


for url in files:
  if url == "":
    continue
  else:
    output_path = "" # @param {type:"string"}
    apiKey = "699996yph6h88a7rc6c1g8"
    parts = url.split('/')
    domain = parts[2]
    filecode = parts[3]
  #  print(parts)
  #  print(domain)
  #  print(filecode)
    #https://katfile.com/api/file/clone?key=699996yph6h88a7rc6c1g8&file_code=zrzac82zifv0
    cloneurl = f"https://{domain}/api/file/clone?key={apiKey}&file_code={filecode}"
    response = requests.get(cloneurl)
    if response.status_code == 200:
        json_data = response.json()
        download_url = json_data.get('result', {}).get('url')
    #    print(download_url)
        parts_final = download_url.split('/')
        filecodex = parts_final[3]
        final_url= f"https://{domain}/api/file/direct_link?key={apiKey}&file_code={filecodex}"
        response = requests.get(final_url)
        if response.status_code == 200:
            json_data = response.json()
            download_url = json_data.get('result', {}).get('url')
         #   print(download_url)
            !wget -P $output_path $download_url
        else:
            print("Error while fetching Katfile API")
    else:
      print("Error while fetching Katfile API")
