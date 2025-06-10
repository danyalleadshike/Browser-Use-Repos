import requests

from unstructured.partition.html import partition_html


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
# Configure settings by clicking the ¦¦¦ button on the right
mutation ScrapingExample {
	goto(url: "https://www.booking.com", waitUntil: networkIdle) {
  status
  time
}
  closeModal: click(
  selector: "button[aria-label='Dismiss sign-in info.']",
  visible: true,
  timeout: 5000
) {
  time
}
  type(
  text: "New York",
  selector: "input[name='ss'][placeholder='Where are you going?']",
  delay: [1, 10]
) {
  selector
}
  submitSearch: click(
  selector: "button[type='submit'][class*='a83ed08757']",
  visible: true
) {
  selector
  time
} waitForSelector(
  selector: "div[data-testid='property-card']",
  timeout: 15000
) {
  time
  selector
} htmlContent: html(
  visible:false
) {
  html
} 
  

  # Click the </> button on the right to export the code,
  # and call it as an API in the chosen language
}
    """,
    "operationName": "ScrapingExample",
}

response = requests.post(endpoint, params=query_string, headers=headers, json=payload)
# print(response.content)



elements = partition_html(text=response.text)
content = "\n\n".join([str(el) for el in elements])
content = [content[i:i + 8000] for i in range(0, len(content), 8000)]

for chunk in content:
    print(chunk)
    print("*"*50)



