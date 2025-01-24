from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random

def setup_webdriver():
    """Set up the Chrome WebDriver with necessary options."""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--user-agent={}'.format(random.choice(["User-Agent1", "User-Agent2"])))

    # Let Selenium manage the driver
    return webdriver.Chrome(options=options)

# Example usage
def main():
    driver = setup_webdriver()
    driver.get("https://www.google.com")
    print("Page title:", driver.title)
    driver.quit()
