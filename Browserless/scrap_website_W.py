import requests
import json
from unstructured.partition.html import partition_html


url = f"https://chrome.browserless.io/content?token=2SNlnW6udnYEzvgcc8c4c81321bf0abc8a652590bb1dbd357"
payload = json.dumps({"url": 'https://www.ebay.com/'})
headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)

elements = partition_html(text=response.text)
content = "\n\n".join([str(el) for el in elements])
content = [content[i:i + 8000] for i in range(0, len(content), 8000)]

for chunk in content:
    print(chunk)
    print("*"*50)