import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time

def automate_download(url, username, password, download_link, timeout=90):
    try:
        # Chrome options for headless browsing
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Use ChromeDriver from PATH if available
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)
        
        # Wait for and fill in username
        username_field = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys(username)
        
        # Wait for and fill in password
        password_field = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys(password)
        
        # Click login button
        login_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "wp-submit-login"))
        )
        login_button.click()
        
        # Wait for login to complete
        WebDriverWait(driver, timeout).until(
            EC.url_changes(url)
        )
        print("Login successful!")

        # Wait for and click the service page button
        service_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 
                'a[href="/product/envato-elements-file-download/"]' + 
                '.btn.btn-color-primary.btn-style-default.btn-style-semi-round.btn-size-small.btn-full-width'))
        )
        service_button.click()
        print("Navigated to service page successfully!")

        # Wait for and fill in download link
        download_input = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "downloadLink"))
        )
        download_input.clear()
        download_input.send_keys(download_link)
        print("Download link entered successfully!")
        time.sleep(3)

        # Click download button
        download_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "downloadButton"))
        )
        download_button.click()
        print("Download button clicked!")

        time.sleep(5)

        def copy_button_visible(driver):
            button = driver.find_element(By.ID, "copyButton")
            return button.is_displayed()

        WebDriverWait(driver, timeout).until(copy_button_visible)
        
        # Click the copy button
        copy_button = driver.find_element(By.ID, "copyButton")
        copy_button.click()
        print("Copy button clicked successfully!")
        time.sleep(30)
        return driver
        
    except TimeoutException:
        print("Timeout waiting for elements to load")
        driver.quit()
        raise
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        driver.quit()
        raise

def main():
    # Direct string assignments
    WEBSITE_URL = "https://stocip.com/login"
    USERNAME = "miguelcantero970@gmail.com"
    PASSWORD = "Reserve85$$"
    DOWNLOAD_LINK = "https://elements.envato.com/cyber-ai-cyber-punk-website-SERFKFT"

    try:
        driver = automate_download(WEBSITE_URL, USERNAME, PASSWORD, DOWNLOAD_LINK)
        # When done, close the browser
        driver.quit()
    except Exception as e:
        print(f"Automation failed: {str(e)}")

if __name__ == "__main__":
    main()
