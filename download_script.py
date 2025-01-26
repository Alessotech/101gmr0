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

            # Click the "Copy" button
            await page.click("#copyButton")
            print("Copy button clicked!")

            # Attempt to retrieve the link from the clipboard
            try:
                clipboard_content = await context.clipboard.read_text()
                if clipboard_content:
                    print(f"Copied link from clipboard: {clipboard_content}")
                else:
                    print("Clipboard is empty or inaccessible.")
            except Exception as e:
                print(f"Clipboard access failed: {e}")

            # If clipboard is empty, check if the link is stored in a DOM element
            try:
                copied_link = await page.input_value("#hiddenInput")  # Replace with actual selector
                print(f"Copied link from DOM element: {copied_link}")
            except Exception as e:
                print(f"Failed to retrieve copied link from DOM: {e}")

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
