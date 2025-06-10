import requests

endpoint = "https://production-sfo.browserless.io/chrome/bql"
query_string = {
    "token": "2SNlnW6udnYEzvgcc8c4c81321bf0abc8a652590bb1dbd357",
    "blockConsentModals": "true",
}
headers = {
    "Content-Type": "application/json",
}
payload = {
    "query": """
# Configure the residential proxy by using a proxy query.
#
# It uses 6 units/MB, and is helpful for getting past bot detectors and captchas.
#

mutation ProxyExample {
  proxy(type: [document, xhr], country: US, sticky: true) {
    time
  }

  goto(url: "https://ipinfo.io/", waitUntil: firstContentfulPaint) {
    status
  }

  # Use the response function to get the response from a request
  response(url: "*ipinfo.io/json*", type: xhr) {
    url
    body
  }

# For help with captchas, look up solve and verify in the docs (the 📕 button, top left)
}
    """,
    "operationName": "ProxyExample",
}

response = requests.post(endpoint, params=query_string, headers=headers, json=payload)
print(response.json())

