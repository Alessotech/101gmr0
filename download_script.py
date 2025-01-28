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
            headless=False,  # Set to False to debug
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--disable-extensions",
            ],
        )
        context = await browser.new_context()
        page = await context.new_page()

        extracted_link = None  # Store the detected download link

        # **Console Listener to Detect Download Link**
        async def console_listener(msg):
            nonlocal extracted_link
            text = msg.text
            print(f"[Browser Console] {text}")  # Print all console messages
            if "video-downloads.elements.envato" in text:  # Adjust the keyword based on actual log format
                extracted_link = text  # Store the detected link
                print(f"Download link detected: {extracted_link}")

        page.on("console", console_listener)  # Attach listener to page

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

            # **WAIT FOR COPY BUTTON TO APPEAR**
            await page.wait_for_selector("#copyButton", timeout=timeout * 1000)  # Change to correct selector
            print("Copy button appeared!")

            # **CLICK COPY BUTTON**
            await page.click("#copyButton")
            print("Copy button clicked!")

            # **WAIT FOR CONSOLE TO LOG THE DOWNLOAD LINK**
            await asyncio.sleep(5)  # Allow some time for the console message to appear

            if extracted_link:
                return {"download_link": extracted_link}
            else:
                return {"message": "No download link detected in console."}

        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            await context.close()
            await browser.close()

# FastAPI route to trigger automation with download_link as a query parameter
@app.get("/automate-download/")
async def automate(download_link: str):
    try:
        result = await automate_download(download_link)
        return {"message": "Automation completed successfully!", "download_link": result["download_link"]}
    except Exception as e:
        return {"error": str(e)}

# Health check route
@app.get("/ping")
async def ping():
    return {"message": "Pong!"}
