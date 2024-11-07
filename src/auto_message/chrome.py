from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
from auto_message.configs import Settings, get_settings
import time

settings: Settings = get_settings()
options = Options()
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)



try:
    # Open Messenger
    driver.get(settings.target_url)
    print(driver.title)

    # Wait for email input field to be clickable
    email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'email'))
    )
    email_input.send_keys(settings.username)

    # Wait for password input field to be clickable
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'pass'))
    )
    password_input.send_keys(settings.password)
    password_input.send_keys(Keys.RETURN)

    # Wait for the search box and enter friend's name
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//input[contains(@placeholder, "Search Messenger")]'))
    )
    search_box.send_keys(settings.chat_name)
    time.sleep(3)  # Wait for the results to load

    # Click on the first search result
    # chat_xpath = f'//a[contains(@href, "{settings.chat_id}") and @role="presentation"]'
    chat_result = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, settings.chat_id))
    )

    # Scroll the element into view and click it
    driver.execute_script("arguments[0].scrollIntoView(true);", chat_result)
    driver.execute_script("arguments[0].click();", chat_result)
    time.sleep(5)
    # Wait for the chat panel to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
    )

    # Find the message input box and send the message
    message_box = driver.find_element(By.XPATH, '//div[@role="textbox"]')
    message_box.click()
    message_box.send_keys(settings.message)
    message_box.send_keys(Keys.RETURN)
    time.sleep(3)

    print("Message sent successfully!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
