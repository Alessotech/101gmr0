from playwright.async_api import async_playwright
import asyncio
import os

async def automate_download(url, username, password, download_link, timeout=90):
    """Automate the download process."""
    async with async_playwright() as p:
        # Launch browser in headless mode with low-resource options
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--disable-extensions",
            ]
        )
        page = await browser.new_page()

        try:
            # Navigate to the login page
            await page.goto(url)

            # Login process
            await page.fill("#username", username)
            await page.fill("#password", password)
            await page.click("#wp-submit-login")

            # Wait for navigation
            await page.wait_for_url(lambda new_url: new_url != url, timeout=timeout * 1000)
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

            # Wait for the copy button
            await page.wait_for_selector("#copyButton", timeout=timeout * 1000)
            await page.click("#copyButton")
            print("Copy button clicked!")

            # Additional wait to simulate user action
            await asyncio.sleep(30)

        except Exception as e:
            print(f"An error occurred: {e}")
            raise

        finally:
            await browser.close()

if __name__ == "__main__":
    # Retrieve sensitive information from environment variables
    WEBSITE_URL = os.getenv("WEBSITE_URL", "https://stocip.com/login")
    USERNAME = os.getenv("USERNAME", "default_user")
    PASSWORD = os.getenv("PASSWORD", "default_password")
    DOWNLOAD_LINK = os.getenv("DOWNLOAD_LINK", "https://elements.envato.com/example-link")

    # Run the automation script
    try:
        asyncio.run(automate_download(WEBSITE_URL, USERNAME, PASSWORD, DOWNLOAD_LINK))
    except Exception as e:
        print(f"Automation failed: {e}")
