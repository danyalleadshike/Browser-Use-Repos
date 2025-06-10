import requests
import json

# Set your Browserless token
BROWSERLESS_TOKEN = "2SNlnW6udnYEzvgcc8c4c81321bf0abc8a652590bb1dbd357"
ENDPOINT = f"https://chrome.browserless.io/scrape?token={BROWSERLESS_TOKEN}"

# Wrap your script in an `elements` list
payload = {
    "elements": [
        {
            "name": "ScrapeEbay",
            "script": """
mutation ScrapeEbay {
  goto(url: "https://www.ebay.com", waitUntil: firstContentfulPaint) {
    status
  }

  typeSearch: type(
    selector: "input[placeholder='Search for anything']"
    text: "laptop"
    delay: [50, 150]
  ) {
    time
  }

  clickSearch: click(selector: "input[type='submit'][value='Search']") {
    time
  }

  waitForNavigation(waitUntil: networkIdle) {
    status
  }

  titles: querySelectorAll(selector: "h3.s-item__title") {
    innerText
  }

  prices: querySelectorAll(selector: ".s-item__price") {
    innerText
  }
}
"""
        }
    ]
}

# Send request
response = requests.post(
    ENDPOINT,
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload)
)

# Process result
if response.status_code == 200:
    data = response.json()[0].get("data", {})
    titles = data.get("titles", [])
    prices = data.get("prices", [])
    for title, price in zip(titles, prices):
        print(f"{title['innerText']} — {price['innerText']}")
else:
    print("Error:", response.status_code, response.text)
