from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright
import asyncio
import re
import os

app = FastAPI()

WEBSITE_URL = "https://stocip.com/login"
USERNAME = "miguelcantero970@gmail.com"
PASSWORD = "Reserve85$$"

DOWNLOAD_DIR = "./downloads"  # Directory to save downloaded files
os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # Ensure the directory exists

async def automate_download(download_link: str, timeout: int = 90):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,  # Must be True for DigitalOcean
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--disable-extensions",
                "--enable-automation",
                "--disable-infobars",
                "--window-size=1920,1080",
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",  # Prevent bot detection
            ],
        )
        context = await browser.new_context(accept_downloads=True)  # Enable download handling
        page = await context.new_page()

        try:
            # Log in to the website
            await page.goto(WEBSITE_URL)
            await page.fill("#username", USERNAME)
            await page.fill("#password", PASSWORD)
            await page.click("#wp-submit-login")
            await page.wait_for_url(lambda new_url: new_url != WEBSITE_URL, timeout=timeout * 1000)
            print("✅ Login successful!")

            # Navigate to the service page
            await page.click('a[href="/product/envato-elements-file-download/"]')
            print("✅ Navigated to service page!")

            # Enter the download link
            await page.fill("#downloadLink", download_link)
            print("✅ Download link entered!")

            # Trigger the download
            download_event = await asyncio.gather(
                page.wait_for_event("download"),  # Wait for the download to start
                page.click("#downloadButton"),   # Trigger the download
            )
            download = download_event[0]

            # Save the downloaded file locally
            download_path = os.path.join(DOWNLOAD_DIR, await download.suggested_filename())
            await download.save_as(download_path)
            print(f"✅ File downloaded: {download_path}")

            return {"message": "✅ Download completed successfully!", "file_path": download_path}

        except Exception as e:
            print(f"❌ An error occurred: {e}")
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            await context.close()
            await browser.close()

@app.get("/automate-download/")
async def automate(download_link: str):
    try:
        result = await automate_download(download_link)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/ping")
async def ping():
    return {"message": "Pong!"}
