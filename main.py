from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import pandas as pd
from datetime import datetime

def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
    options.add_argument('--window-size=1920,1080')
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=options)
    return driver

def wait_for_element(driver, by, value, timeout=20):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {value}")
        return None

def scrape_page_with_retry(driver, url, max_retries=3):
    for attempt in range(max_retries):
        try:
            print(f"\nAttempt {attempt + 1} of {max_retries} for URL: {url}")
            
            if attempt > 0:
                print("Recreating browser session...")
                driver.quit()
                driver = setup_driver()
            
            print("Loading page...")
            driver.get(url)
            
            # Print initial page info
            print(f"Initial page title: {driver.title}")
            print("Waiting for page to stabilize...")
            time.sleep(10)  # Increased initial wait time
            
            print(f"Current URL: {driver.current_url}")
            print(f"Final page title: {driver.title}")
            
            # Check if page loaded properly
            if not driver.title or len(driver.page_source) < 1000:
                print("Page might not have loaded properly. Retrying...")
                continue
            
            print("Looking for property cards...")
            try:
                # Wait for any property-related element
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "re__card-info"))
                )
            except TimeoutException:
                print("Timeout waiting for property cards. Page source preview:")
                print(driver.page_source[:1000])
                if attempt < max_retries - 1:
                    continue
            
            # Find all property cards
            cards = driver.find_elements(By.CLASS_NAME, "re__card-info")
            
            if not cards:
                print("No property cards found. Retrying...")
                if attempt < max_retries - 1:
                    continue
            
            print(f"Found {len(cards)} property cards")
            properties = []
            
            for index, card in enumerate(cards, 1):
                try:
                    property_data = {}
                    print(f"\nProcessing property {index}/{len(cards)}")
                    
                    # Extract title
                    try:
                        title_elem = card.find_element(By.CLASS_NAME, "js__card-title")
                        property_data['Title'] = title_elem.text.strip()
                        print(f"Title found: {property_data['Title'][:50]}...")
                    except NoSuchElementException:
                        property_data['Title'] = "N/A"
                        print("Title not found")
                    
                    # Extract price
                    try:
                        price_elem = card.find_element(By.CLASS_NAME, "re__card-config-price")
                        property_data['Price'] = price_elem.text.strip()
                        print(f"Price found: {property_data['Price']}")
                    except NoSuchElementException:
                        property_data['Price'] = "N/A"
                    
                    # Extract area
                    try:
                        area_elem = card.find_element(By.CLASS_NAME, "re__card-config-area")
                        property_data['Area'] = area_elem.text.strip()
                        print(f"Area found: {property_data['Area']}")
                    except NoSuchElementException:
                        property_data['Area'] = "N/A"
                    
                    # Extract price per m2
                    try:
                        price_per_m2_elem = card.find_element(By.CLASS_NAME, "re__card-config-price_per_m2")
                        property_data['Price_per_m2'] = price_per_m2_elem.text.strip()
                        print(f"Price per m2 found: {property_data['Price_per_m2']}")
                    except NoSuchElementException:
                        property_data['Price_per_m2'] = "N/A"
                    
                    # Extract location
                    try:
                        location_elem = card.find_element(By.CLASS_NAME, "re__card-location")
                        location_span = location_elem.find_elements(By.TAG_NAME, "span")[-1]
                        property_data['Location'] = location_span.text.strip()
                        print(f"Location found: {property_data['Location']}")
                    except (NoSuchElementException, IndexError):
                        property_data['Location'] = "N/A"
                    
                    properties.append(property_data)
                    print(f"Successfully scraped property {index}")
                    
                except Exception as e:
                    print(f"Error scraping property {index}: {str(e)}")
                    continue
            
            if properties:
                return properties, driver
            
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                print("Waiting 20 seconds before retry...")
                time.sleep(20)
            continue
    
    return [], driver

def main():
    driver = setup_driver()
    all_properties = []
    base_url = "https://batdongsan.com.vn/ban-can-ho-chung-cu-quan-1/p{}"
    
    try:
        for page in range(1, 11):
            properties, driver = scrape_page_with_retry(driver, base_url.format(page))
            
            if properties:
                all_properties.extend(properties)
                print(f"Successfully scraped {len(properties)} properties from page {page}")
            else:
                print(f"No properties found on page {page} after all retries")
            
            if page < 10:
                delay = 20  # Fixed delay between pages
                print(f"Waiting {delay} seconds before next page...")
                time.sleep(delay)
    
    except Exception as e:
        print(f"An error occurred in main: {str(e)}")
    
    finally:
        try:
            driver.quit()
        except:
            pass
    
    if all_properties:
        df = pd.DataFrame(all_properties)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"district1_properties_{timestamp}.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"\nData saved to {csv_filename}")
        print(f"Total properties scraped: {len(all_properties)}")
    else:
        print("\nNo properties were scraped. Please check the website structure or try again later.")

if __name__ == "__main__":
    main()