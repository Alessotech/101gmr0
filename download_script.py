from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

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

@app.get("/debug")
async def debug():
    """Debug route to check if ChromeDriver and Chromium are properly installed."""
    try:
        # Attempt to initialize the WebDriver
        driver = setup_webdriver()
        
        # Open a simple page
        driver.get("https://www.google.com")
        
        # Get page title to verify everything is working
        title = driver.title
        driver.quit()
        return {
            "message": "ChromeDriver and Selenium are working!",
            "page_title": title,
            "chrome_binary": os.getenv("CHROME_BIN", "Not set"),
            "chromedriver_path": os.getenv("CHROMEDRIVER_PATH", "Not set")
        }
    except Exception as e:
        return {
            "error": str(e),
            "chrome_binary": os.getenv("CHROME_BIN", "Not set"),
            "chromedriver_path": os.getenv("CHROMEDRIVER_PATH", "Not set")
        }

@app.post("/download/")
async def process_download(request: DownloadRequest):
    """Process the download request."""
    # Your original download logic here...
    return {"message": "Download route is working."}

def main():
    """Run the FastAPI app with Uvicorn."""
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
