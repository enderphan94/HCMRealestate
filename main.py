from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=options)

try:
    print("Accessing the website...")
    driver.get("https://batdongsan.com.vn/ban-can-ho-chung-cu-scenic-valley-1?sortValue=2")
    
    time.sleep(5)
    
    print("Waiting for elements to load...")
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "re__card-info"))
        )
        print("Found element:", element.text)
    except TimeoutException:
        print("Timeout waiting for elements. Current page source:")
        print(driver.page_source[:1000])  
        raise
    
    cards = driver.find_elements(By.CLASS_NAME, "re__card-info")

    for card in cards:
        title = card.find_element(By.CLASS_NAME, "re__card-title").text
        price = card.find_element(By.CLASS_NAME, "re__card-config-price").text
        area = card.find_element(By.CLASS_NAME, "re__card-config-area").text
        price_per_m2 = card.find_element(By.CLASS_NAME, "re__card-config-price_per_m2").text
        location = card.find_element(By.CLASS_NAME, "re__card-location").text

        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Area: {area}")
        print(f"Price per m²: {price_per_m2}")
        print(f"Location: {location}")
        print("-" * 40)

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    print("Closing browser...")
    driver.quit()