import requests

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
    "url": "https://www.google.com"
}

response = requests.post(
    f"{endpoint}?token={token}",
    json={"query": query, "variables": variables}
)

print(response.json())