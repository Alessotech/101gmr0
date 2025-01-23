# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.common.keys import Keys
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC

# # import time

# # cokkcc_count= "cookies"
# # pr_price_prefix="productPrice"
# # proud__prefix="product"

# # driver = webdriver.Chrome()
# # driver.get("https://orteil.dashnet.org/cookieclicker/")


# # time.sleep(3)  # Wait for the page to load fully
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import time


# # Step 2: Configure ChromeOptions
# chrome_options = Options()

# # Step 3: Initialize WebDriver with the configured options
# driver = webdriver.Chrome(options=chrome_options)

# # Step 4: Open any initial page to initialize Chrome context
# driver.get("https://www.google.com")
#   # Wait for the browser to initialize

# # Step 5: Trigger the extension popup using Chrome DevTools Protocol

#     # Step 6: Switch to the popup's window (if it opens in a new context)
#     # You can interact with it as needed
#     # Example: Find and click a button
#     # time.sleep(2)  # Wait for the popup to load
#     # driver.switch_to.window(driver.window_handles[-1])  # Switch to the last opened window
#     # paste_button = driver.find_element(By.ID, "id_session_paste")  # Replace with actual ID
#     # paste_button.click()
#     # print("Clicked the button in the popup successfully!")


# # Step 7: Cleanup
# time.sleep(16)  # Allow time to verify the interaction
# # driver.quit()















# # Now the browser should be logged in or have the cookies applied



# # input_element=driver.find_element(By.ID, "langSelect-EN")
# # # input_element.send_keys("aleso store" + Keys.ENTER)
# # input_element.click()

# # WebDriverWait(driver, 80).until(
# #     EC.presence_of_all_elements_located((By.ID, "bigCookie"))
# # )

# # cok_element=driver.find_element(By.ID , "bigCookie")
# # # input_element.send_keys("aleso store" + Keys.ENTER)
# # cok_element.click()

# # while True:
# #     cok_element.click()
# #     cokie_ds=driver.find_element(By.ID, cokkcc_count).text.split(" ")[0]
# #     cokie_ds= int(cokie_ds.replace(",",""))
# #     print(cokie_ds)
   
# #     for i in range(4):
# #         pr__prefix=driver.find_element(By.ID,pr_price_prefix + str(i)).text

# #         if not pr__prefix.isdigit():
# #             continue
# #         pr__prefix= int(pr__prefix)
# #         # print(pr__prefix)

# #         if cokie_ds>=pr__prefix:
        
# #              prodc=driver.find_element(By.ID,proud__prefix + str(i))
# #              prodc.click()
# #              break
            



        


# # link =driver.find_element(By.PARTIAL_LINK_TEXT, "Hermosillo - Aleso Store")
# # link.click()



# # driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def automate_download(url, username, password, download_link, timeout=90):
    """
    Login to website, navigate to service page, and handle download process
    
    Args:
        url (str): Website URL
        username (str): Username or email
        password (str): Password
        download_link (str): The download link to be pasted
        timeout (int): Maximum time to wait for elements (default 10 seconds)
    """
    try:
        # Initialize the webdriver (Chrome in this example)
        driver = webdriver.Chrome()
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

# Example usage
if __name__ == "__main__":
    # Replace these with actual values
    WEBSITE_URL = "https://stocip.com/login"
    USERNAME = "miguelcantero970@gmail.com"
    PASSWORD = "Reserve85$$"
    DOWNLOAD_LINK = "https://elements.envato.com/cyber-ai-cyber-punk-website-SERFKFT"

    try:
        driver = automate_download(WEBSITE_URL, USERNAME, PASSWORD, DOWNLOAD_LINK)
        # Continue with other automated tasks here
        
        # When done, close the browser
        # driver.quit()
    except Exception as e:
        print(f"Automation failed: {str(e)}")