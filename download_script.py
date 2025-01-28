from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright
import asyncio
import re

app = FastAPI()

# Hardcoded constants
WEBSITE_URL = "https://stocip.com/login"
USERNAME = "miguelcantero970@gmail.com"
PASSWORD = "Reserve85$$"

async def automate_download(download_link: str, timeout: int = 90):
    async with async_playwright() as p:
        # RUNNING IN NON-HEADLESS MODE (Since it's on DigitalOcean)
        browser = await p.chromium.launch(
            headless=False,  # RUN WITH Xvfb (Virtual Display)
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--disable-extensions",
                "--use-gl=egl",
                "--enable-automation",
                "--disable-infobars",
                "--enable-features=ClipboardAPI",
            ],
        )
        context = await browser.new_context(
            permissions=["clipboard-read", "clipboard-write"]  # Ensure clipboard access
        )
        page = await context.new_page()

        extracted_link = None  # Store detected download link

        # Console Listener
        async def console_listener(msg):
            nonlocal extracted_link
            text = msg.text
            print(f"[Browser Console] {text}")
            match = re.search(r'https://elements.envato.com/[^\s"\']+', text)
            if match:
                extracted_link = match.group(0)
                print(f"Download link detected: {extracted_link}")

        page.on("console", console_listener)

        try:
            await page.goto(WEBSITE_URL)
            await page.fill("#username", USERNAME)
            await page.fill("#password", PASSWORD)
            await page.click("#wp-submit-login")

            await page.wait_for_url(lambda new_url: new_url != WEBSITE_URL, timeout=timeout * 1000)
            print("Login successful!")

            await page.click('a[href="/product/envato-elements-file-download/"]')
            print("Navigated to service page!")

            await page.fill("#downloadLink", download_link)
            print("Download link entered!")

            await page.click("#downloadButton")
            print("Download button clicked!")

            # Wait for Copy Button
            await page.wait_for_selector("#copyButton", timeout=timeout * 1000)
            print("Copy button appeared!")

            # Click Copy Button Using JavaScript
            await page.evaluate("document.querySelector('#copyButton').click();")
            print("Copy button clicked!")

            # Wait for Console to Log the Download Link
            await asyncio.sleep(5)

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

@app.get("/automate-download/")
async def automate(download_link: str):
    try:
        result = await automate_download(download_link)
        return {"message": "Automation completed successfully!", "download_link": result["download_link"]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/ping")
async def ping():
    return {"message": "Pong!"}
