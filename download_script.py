from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random

# Initialize FastAPI app
app = FastAPI()

# Set up the WebDriver
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

    # Let Selenium manage the driver
    return webdriver.Chrome(options=options)

# Example route to use Selenium
@app.get("/")
async def root():
    """Root endpoint to test WebDriver."""
    try:
        driver = setup_webdriver()
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        return {"message": "WebDriver is working!", "page_title": title}
    except Exception as e:
        return {"error": str(e)}

# Another example route for testing
@app.get("/ping")
async def ping():
    """Ping endpoint to check server health."""
    return {"message": "Pong!"}
