from fastapi import FastAPI
from playwright.async_api import async_playwright
import random

# Initialize FastAPI app
app = FastAPI()

# List of user agents for randomization
USER_AGENTS = ["User-Agent1", "User-Agent2"]

async def fetch_page_title(url: str):
    """Fetch the page title using Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,  # Run in headless mode
            args=[
                "--no-sandbox",  # Required for Docker containers
                "--disable-dev-shm-usage",  # Prevent shared memory issues
                "--disable-gpu",  # Disable GPU rendering
                "--disable-extensions",
                "--disable-infobars",
                "--disable-background-networking",
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--ignore-certificate-errors",
                f"--user-agent={random.choice(USER_AGENTS)}"  # Random user agent
            ]
        )
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=10000)  # 10-second timeout for loading
            title = await page.title()
        finally:
            await browser.close()
        return title

@app.get("/")
async def root():
    """Test route to verify Playwright setup."""
    try:
        title = await fetch_page_title("https://www.google.com")
        return {"message": "Playwright is working!", "page_title": title}
    except Exception as e:
        return {"error": str(e)}

@app.get("/ping")
async def ping():
    """Health check endpoint."""
    return {"message": "Pong!"}
