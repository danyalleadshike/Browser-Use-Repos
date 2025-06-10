# https://deviceandbrowserinfo.com/are_you_a_bot

import requests
import base64 

endpoint = "https://production-sfo.browserless.io/chromium/bql"
token = "2SNlnW6udnYEzvgcc8c4c81321bf0abc8a652590bb1dbd357"

query = """
mutation Screenshot($url: String!) {
  goto(url: $url, waitUntil: load) {
    status
  }
  screenshot(type: jpeg) {
    base64
  }
}
"""

variables = {
    "url": "https://www.netflix.com/pk/"
}

response = requests.post(
    f"{endpoint}?token={token}",
    json={"query": query, "variables": variables}
)

# print(response.json())


# Parse and decode the image
data = response.json()
try:
    base64_img = data['data']['screenshot']['base64']
    with open("netflix.jpg", "wb") as f:
        f.write(base64.b64decode(base64_img))
    print("✅ Screenshot saved as screenshot.jpg")
except KeyError:
    print("❌ Failed to get screenshot:", data)