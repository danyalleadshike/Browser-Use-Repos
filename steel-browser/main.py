import asyncio
from steel import Steel
from browser_use import Agent, Controller
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import time

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

# Initialize the Steel client with API key
# Replace "YOUR_STEEL_API_KEY" with your actual API key
client = Steel(steel_api_key=os.getenv("STEEL_API_KEY"))

# Create a Steel session
print("Creating Steel session...")
session = client.sessions.create(
    # use_proxy=True,
    # solve_captcha=True,
)
print(f"Session created at {session.session_viewer_url}")
steel_key = os.getenv('STEEL_API_KEY')
print(steel_key)

controller = Controller()

# Connect browser-use to Steel
# Replace YOUR_STEEL_API_KEY with your actual API key
cdp_url = f"wss://connect.steel.dev?apiKey={steel_key}&sessionId={session.id}"
browser = Browser(config=BrowserConfig(cdp_url=cdp_url))
browser_context = BrowserContext(browser=browser)

browser_session = BrowserSession(
	headless=False,
	cdp_url=cdp_url
)


model = ChatGoogleGenerativeAI( # Changed model initialization
    model="gemini-2.0-flash",  # Or "gemini-1.5-pro" or other suitable Gemini model
    # temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY") # Use environment variable for API key
)

task = "Go to docs.steel.dev, open the changelog, and tell me what's new."

# agent = Agent(
#     task=task,
#     llm=model,
#     # browser=browser,
#     browser_context=browser_context,
#     browser_session = browser_session
# )
agent = Agent(
		task=task,
		llm=model,
		controller=controller,
		browser_session=browser_session,
	)


async def main():
  try:
      # Run the agent
      print("Running the agent...")
      await agent.run()
      
        # await browser_session.close()
      print("Task completed!")
      
  except Exception as e:
      print(f"An error occurred: {e}")
  finally:
      time.sleep(10)
      
      # Clean up resources
      if browser:
          await browser.close()
          print("Browser closed")
      if session:
          client.sessions.release(session.id)
          print("Session released")
      print("Done!")

# Run the async main function
if __name__ == '__main__':
    asyncio.run(main())