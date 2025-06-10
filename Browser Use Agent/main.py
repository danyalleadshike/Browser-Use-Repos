from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserSession, Browser, BrowserConfig
from dotenv import load_dotenv
import asyncio

# Read GOOGLE_API_KEY into env
load_dotenv()

# Initialize the model
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

initial_actions = [
	{'open_tab': {'url': 'https://www.google.com'}},
	{'open_tab': {'url': 'https://en.wikipedia.org/wiki/Randomness'}},
	{'scroll_down': {'amount': 1000}},
]

browser_session = BrowserSession(
    # Path to a specific Chromium-based executable (optional)
    executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 

    # Use a specific data directory on disk (optional)
    user_data_dir='C:\\Users\\HP\\AppData\\Local\\Google\\Chrome\\User Data\\Default',
    # ... any other BrowserProfile or playwright launch_persistnet_context config...
    # headless=False,
)
browser = Browser(
    config=BrowserConfig(
        chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    )
)


async def main():
    agent = Agent(
    task="Price of a G Wagon in Pakistan",
    llm=llm,
    # browser = browser,
    browser_session = browser_session,
    enable_memory=False
)
    await agent.run()

asyncio.run(main())