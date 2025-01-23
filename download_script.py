from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import uvicorn
import os
import time

app = FastAPI()

class DownloadRequest(BaseModel):
    website_url: str
    username: str
    password: str
    download_link: str

def automate_download(url, username, password, download_link, timeout=90):
    try:
        # Chrome options for headless browsing
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        # Login process
        username_field = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys(username)
        
        password_field = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys(password)
        
        login_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "wp-submit-login"))
        )
        login_button.click()
        
        WebDriverWait(driver, timeout).until(
            EC.url_changes(url)
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
        
        def copy_button_visible(driver):
            button = driver.find_element(By.ID, "copyButton")
            return button.is_displayed()
        
        WebDriverWait(driver, timeout).until(copy_button_visible)
        
        # Click copy button
        copy_button = driver.find_element(By.ID, "copyButton")
        copy_button.click()
        
        # You might want to extract the final download link here
        # This is a placeholder - modify based on actual website behavior
        final_download_link = driver.current_url
        
        driver.quit()
        return final_download_link
        
    except TimeoutException:
        driver.quit()
        raise HTTPException(status_code=408, detail="Timeout during download process")
    except Exception as e:
        driver.quit()
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.post("/download/")
async def process_download(request: DownloadRequest):
    try:
        final_link = automate_download(
            request.website_url, 
            request.username, 
            request.password, 
            request.download_link
        )
        return {"download_link": final_link}
    except HTTPException as http_exc:
        raise http_exc

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
