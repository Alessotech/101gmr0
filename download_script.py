from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import uvicorn
import os
import time

app = FastAPI()

class DownloadRequest(BaseModel):
    download_link: str

def setup_webdriver():
    """Set up the Chrome WebDriver with necessary options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.binary_location = os.getenv("CHROME_BIN", "/usr/bin/chromium")
    
    service = Service(os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver"))
    return webdriver.Chrome(service=service, options=chrome_options)

def automate_download(download_link, timeout=90):
    """Automate the download process."""
    driver = None
    try:
        # Load credentials from environment variables
        URL = "https://stocip.com/login"
        USERNAME = os.getenv("STOCIP_USERNAME")
        PASSWORD = os.getenv("STOCIP_PASSWORD")

        if not USERNAME or not PASSWORD:
            raise HTTPException(status_code=500, detail="Missing credentials in environment variables.")

        driver = setup_webdriver()
        driver.get(URL)
        
        # Login process
        username_field = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys(USERNAME)
        
        password_field = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys(PASSWORD)
        
        login_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "wp-submit-login"))
        )
        login_button.click()
        
        WebDriverWait(driver, timeout).until(
            EC.url_changes(URL)
        )
        
        # Navigate to service page
        service_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 
                'a[href="/product/envato-elements-file-download/"]' + 
                '.btn.btn-color-primary.btn-style-default.btn-style-semi-round.btn-size-small.btn-full-width'))
        )
        service_button.click()
        
        # Fill download link
        download_input = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "downloadLink"))
        )
        download_input.clear()
        download_input.send_keys(download_link)
        time.sleep(3)
        
        # Click download button
        download_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "downloadButton"))
        )
        download_button.click()
        
        time.sleep(5)
        
        # Wait for copy button
        def copy_button_visible(driver):
            button = driver.find_element(By.ID, "copyButton")
            return button.is_displayed()
        
        WebDriverWait(driver, timeout).until(copy_button_visible)
        
        # Extract final download link
        copy_button = driver.find_element(By.ID, "copyButton")
        final_download_link = copy_button.get_attribute("data-clipboard-text")
        
        driver.quit()
        return final_download_link
        
    except Exception as e:
        if driver:
            driver.quit()
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.post("/download/")
async def process_download(request: DownloadRequest):
    """Process the download request."""
    try:
        final_link = automate_download(request.download_link)
        return {"download_link": final_link}
    except HTTPException as http_exc:
        raise http_exc

def main():
    """Run the FastAPI app with Uvicorn."""
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
