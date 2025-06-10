# This script demonstrates how to:
#- create a Steel session
#- connect to that session with Playwright
#- and scrape Hacker News.

from playwright.sync_api import sync_playwright
from steel import Steel
import os
import time

# Initialize Steel client with API key
# Replace "YOUR_STEEL_API_KEY" with your actual API key
client = Steel(steel_api_key=os.getenv("STEEL_API_KEY"))

def main():
    session = None
    browser = None
    try:
        # Create a Steel session
        print("Creating Steel session...")
        session = client.sessions.create()
        print(f"Session created at {session.session_viewer_url}")
        
        # Connect Playwright to the Steel session
        playwright = sync_playwright().start()
        browser = playwright.chromium.connect_over_cdp(
            f"wss://connect.steel.dev?apiKey={os.getenv('STEEL_API_KEY')}&sessionId={session.id}"
        )
        print("Connected to browser via Playwright")
        
        # Create page at existing context to ensure session is recorded
        current_context = browser.contexts[0]
        page = current_context.pages[0]
        
        # ============ Your Automations Go Here! =============

        # Example script - Navigate to Hacker News and extract the top 5 stories
        print("Navigating to Hacker News...")
        page.goto("https://news.ycombinator.com", wait_until="networkidle")

        # Find all story rows
        story_rows = page.locator("tr.athing").all()[:5]  # Get first 5 stories

        # Extract the top 5 stories using Playwright's locators
        print("\nTop 5 Hacker News Stories:")
        for i, row in enumerate(story_rows, 1):
            # Get the title and link from the story row
            title_element = row.locator(".titleline > a")
            title = title_element.text_content()
            link = title_element.get_attribute("href")

            # Get points from the following row
            points_element = row.locator(
                "xpath=following-sibling::tr[1]").locator(".score")
            points = points_element.text_content().split(
            )[0] if points_element.count() > 0 else "0"

            # Print the story details
            print(f"\n{i}. {title}")
            print(f"   Link: {link}")
            print(f"   Points: {points}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(10)

        # Clean up resources
        if browser:
            browser.close()
            print("Browser closed")
        if session:
            client.sessions.release(session.id)
            print("Session released")
        print("Done!")

# Run the script
if __name__ == "__main__":
    main()