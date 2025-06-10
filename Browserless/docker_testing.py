import requests
import json
import base64 # For decoding if screenshot is base64 encoded

# --- Configuration ---
BROWSERLESS_BASE_URL = "http://localhost:3000"  # Your browserless instance URL
SCREENSHOT_ENDPOINT = f"{BROWSERLESS_BASE_URL}/chromium/screenshot"
TARGET_URL = "https://www.amazon.com" # Replace with the URL you want to screenshot
BROWSERLESS_API_TOKEN = None  # Replace with your token if you have one, e.g., "YOUR_TOKEN"
OUTPUT_FILENAME = "screenshot.jpeg"

# --- Payload for screenshot ---
# We request a full-page PNG, encoded in base64 to be returned in the JSON.
# Alternatively, you can omit "encoding": "base64" to get raw image binary.
screenshot_payload = {
    "url": TARGET_URL,
    "options": {
        "type": "jpeg",           # 'jpeg' is also an option
        "fullPage": True,        # Capture the full scrollable page
        "encoding": "base64",    # Get base64 string in response.
                                 # If omitted or set to "binary",
                                 # response content will be the raw image.
        "quality": 75,         # Only for jpeg (0-100)
        # "omitBackground": False
    },
    "gotoOptions": {
        "timeout": 30000,        # Page navigation timeout in milliseconds
        "waitUntil": ["networkidle0"] # Wait until network is idle
    },
    "viewport": {                # Optional: Set a specific viewport size
        "width": 1920,
        "height": 1080
    }
}

# --- Headers and Params ---
headers = {
    "Content-Type": "application/json"
}
params = {}
# if BROWSERLESS_API_TOKEN:
#     params["token"] = BROWSERLESS_API_TOKEN

# --- Send the request ---
print(f"🚀 Sending screenshot request for: {TARGET_URL}")

try:
    response = requests.post(SCREENSHOT_ENDPOINT, headers=headers, params=params, json=screenshot_payload, timeout=60) # 60-second timeout

    if response.status_code == 200:
        # Check if the response is base64 encoded (as requested in payload)
        # The browserless /screenshot endpoint might also return raw binary if 'encoding' is not 'base64'
        # or if the Content-Type suggests it (e.g., image/png)
        content_type = response.headers.get("Content-Type", "")
        print("Response: ", response)
        print("Content type: ", content_type)

        if screenshot_payload.get("options", {}).get("encoding") == "base64" and "application/json" in content_type:
            print("✅ Screenshot request successful (base64 in JSON).")
            response_data = response.json()
            print(response_data)
            # Assuming the base64 data is directly in the response or a specific key like 'data'
            # The browserless docs for /screenshot imply the 200 response can be text/plain (base64) or binary.
            # If it's in a JSON structure, you'd need to adapt.
            # Let's assume the base64 string is the direct body for this case (based on "text/plain base64 encoded body")
            # or within a known JSON key if Content-Type is application/json.
            # The sample payload in the docs results in a raw binary if encoding is not specified,
            # or a JSON response with the image data if `options.encoding: 'base64'` *was* used.
            # The actual response structure for base64 via /screenshot might vary slightly.
            # For the given payload example, Browserless typically returns raw image data if encoding is not base64,
            # or if encoding is base64, it may return a JSON object containing the base64 string.
            # Let's assume it sends the base64 string directly as text/plain or in a simple JSON.

            # If the API returns a JSON with the base64 string:
            # Example: response_data = response.json(); screenshot_base64 = response_data.get('data') or response_data.get('screenshot')
            # For now, let's assume it's the raw response text if it's text/plain.
            # If it's JSON, you'd parse it. The example /screenshot payload doesn't show a JSON structure for the 200 response body.
            # It says "Response can either be a text/plain base64 encoded body or a binary stream".
            # If you set "options": {"encoding": "base64"}, it might send it as text/plain.

            screenshot_base64_data = response.text # Assuming text/plain base64
            # If it were JSON like: { "data": "base64string..." }, you'd do:
            # screenshot_base64_data = response.json()['data']

            try:
                screenshot_bytes = base64.b64decode(screenshot_base64_data)
                with open(OUTPUT_FILENAME, "wb") as f:
                    f.write(screenshot_bytes)
                print(f"📸 Screenshot saved as '{OUTPUT_FILENAME}' from base64 data.")
            except Exception as e:
                print(f"❌ Error decoding/saving base64 screenshot: {e}")

        elif "image" in content_type: # e.g. "image/png" or "image/jpeg"
            print("✅ Screenshot request successful (binary image data).")
            with open(OUTPUT_FILENAME, "wb") as f:
                f.write(response.content)
            print(f"📸 Screenshot saved as '{OUTPUT_FILENAME}' from binary stream.")
        else:
            # Fallback for unexpected content type but 200 OK
            print(f"✅ Screenshot request returned 200 OK, but with unexpected Content-Type: {content_type}.")
            print("Raw response text:", response.text[:200] + "...") # Print start of text


    else:
        print(f"❌ Screenshot request failed with status code: {response.status_code}")
        try:
            print("Error response:", response.json())
        except json.JSONDecodeError:
            print("Error response:", response.text)

except requests.exceptions.RequestException as e:
    print(f"❌ An error occurred during the screenshot request: {e}")