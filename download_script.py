from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright
import asyncio

app = FastAPI()

# Hardcoded constants
WEBSITE_URL = "https://stocip.com/login"
USERNAME = "miguelcantero970@gmail.com"
PASSWORD = "Reserve85$$"

# Automation function using Playwright
async def automate_download(download_link: str, timeout: int = 90):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--disable-extensions",
            ],
        )
        context = await browser.new_context()  # New browser context for clipboard access
        page = await context.new_page()

        try:
            # Navigate to the login page
            await page.goto(WEBSITE_URL)

            # Login process
            await page.fill("#username", USERNAME)
            await page.fill("#password", PASSWORD)
            await page.click("#wp-submit-login")

            # Wait for navigation
            await page.wait_for_url(lambda new_url: new_url != WEBSITE_URL, timeout=timeout * 1000)
            print("Login successful!")

            # Navigate to the service page
            await page.click('a[href="/product/envato-elements-file-download/"]')
            print("Navigated to service page!")

            # Enter the download link
            await page.fill("#downloadLink", download_link)
            print("Download link entered!")

            # Click the download button
            await page.click("#downloadButton")
            print("Download button clicked!")

            # Wait for the "Copy" button
            await page.wait_for_selector("#copyButton", timeout=timeout * 1000)

            # Delay before clicking "Copy" button
            await asyncio.sleep(5)
            print("Waiting for 5 seconds before clicking 'Copy' button...")
            
async def get_new_tab_url():
    """Fetches the URL from a new tab opened by clicking a specific button."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Set headless=False to see the browser action
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.click("#downloadButton")  # Adjust the selector to your specific button
            print("Download xxbutton clicked!")

            # Prepare to catch the new tab that opens
            new_page_promise = context.wait_for_event('page')

            # Trigger the action that opens the new tab
            
            # Wait for the new tab to open
            new_page = await new_page_promise
            await new_page.wait_for_load_state('domcontentloaded')
            new_tab_url = new_page.url  # Capture the URL from the new tab
            

            # Additional wait after copying
            await asyncio.sleep(5)
            print("Waited an additional 5 seconds after copying the link.")

        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            await browser.close()

# FastAPI route to trigger automation with download_link as a query parameter
@app.get("/automate-download/")
async def automate(download_link: str):
    try:
        await automate_download(download_link)
        return {"message": "Automation completed successfully!", "link": download_link}
    except Exception as e:
        return {"error": str(e)}

# Health check route
@app.get("/ping")
async def ping():
    return {"message": "Pong!"}
