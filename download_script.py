from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import random

# Initialize FastAPI app
app = FastAPI()

def setup_webdriver():
    """Set up the Chrome WebDriver with necessary options."""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--user-agent={}'.format(random.choice(["User-Agent1", "User-Agent2"])))

    # Use the Service class to specify the ChromeDriver path
    chromedriver_path = "/opt/render/project/.render/chromedriver"  # Path to ChromeDriver
    service = Service(chromedriver_path)

    return webdriver.Chrome(service=service, options=options)

@app.get("/")
async def root():
    """Test route to verify ChromeDriver setup."""
    try:
        driver = setup_webdriver()
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        return {"message": "WebDriver is working!", "page_title": title}
    except Exception as e:
        return {"error": str(e)}

@app.get("/ping")
async def ping():
    """Health check endpoint."""
    return {"message": "Pong!"}
