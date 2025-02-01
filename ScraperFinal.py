from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd

# Function to validate website URLs
def is_valid_website(website):
    valid_extensions = (".com", ".in", ".org", ".net", ".edu", ".gov")
    return website.strip().endswith(valid_extensions)

# Function to scrape travel and tourism companies in Kochi
def scrape_travel_companies(limit=None):
    # Set up Selenium WebDriver
    service = Service("chromedriver.exe")  # Replace with the path to your ChromeDriver
    driver = webdriver.Chrome(service=service)

    try:
        # Open Google Maps and search for travel and tourism companies in Kochi
        driver.get("https://www.google.com/maps")
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys("Tourism and travel companies in Kochi")
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        # Initialize variables for scrolling and fetching results
        action = ActionChains(driver)
        scroll_pause_time = 2
        results = driver.find_elements(By.CLASS_NAME, "hfpxzc")
        le = 0  # Counter to detect stalled scrolling

        # Scroll and load more results until the limit is reached or all results are loaded
        while (limit is None or len(results) < limit) and le <= 20:
            print(f"Current results: {len(results)}")
            prev_len = len(results)

            # Scroll down to load more results
            if results:
                scroll_origin = ScrollOrigin.from_element(results[-1])
                action.scroll_from_origin(scroll_origin, 0, 1000).perform()
                time.sleep(scroll_pause_time)

            results = driver.find_elements(By.CLASS_NAME, "hfpxzc")

            # Check if scrolling has stalled
            if len(results) == prev_len:
                le += 1
            else:
                le = 0

        # List to store all extracted businesses
        businesses = []

        # Iterate over each result and extract data
        for i, result in enumerate(results):
            if limit and i >= limit:
                break

            try:
                # Click on the result to load details
                action.move_to_element(result).perform()
                result.click()
                #Change this to configure how long you want to wait before selecting the next result // Increase value if internest speed is low hehe!!
                time.sleep(5)

                # Parse the page source with BeautifulSoup
                soup = BeautifulSoup(driver.page_source, "html.parser")

                # Extract business details
                name_tag = soup.find("h1", {"class": "DUwDvf lfPIob"})
                name = name_tag.text if name_tag else "No name"

                info_tags = soup.find_all("div", {"class": "Io6YTe fontBodyMedium kR99db fdkmkc"})

                phone = info_tags[2].text if (len(info_tags) > 2 and info_tags[2].text.strip().startswith("0")) else "No phone"
                address = info_tags[0].text if len(info_tags) > 0 else "No address"
                raw_website = info_tags[1].text.strip() if len(info_tags) > 1 else ""
                website = raw_website if is_valid_website(raw_website) else "No website"

                # Append the data to the businesses list
                businesses.append({
                    "Name": name,
                    "Phone": phone,
                    "Address": address,
                    "Website": website,
                })

                # Save data to a CSV file after each business
                pd.DataFrame(businesses).to_csv("Tourism_and_Travel_Companies_in_Kochi.csv", index=False)

                print(f"Scraped: {name}, {phone}, {address}, {website}")

            except Exception as e:
                print("Error while processing a result:", e)
                continue

    finally:
        # Close the WebDriver
        driver.quit()

    print("Scraping completed. Data saved to Tourism_and_Travel_Companies_in_Kochi.csv.")

# Example usage
# Specify a limit (e.g., 50) or leave it as None to scrape all available results
scrape_travel_companies(limit=50)
