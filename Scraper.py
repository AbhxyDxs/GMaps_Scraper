from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd

purpose = "TCS Kerala"

#Function to validate websites that fetched
def is_valid_website(website):
    valid_extensions = (".com", ".in", ".org", ".net", ".edu", ".gov")
    return website.strip().endswith(valid_extensions)

#Main function
def scrape_travel_companies(limit=None):
    #Selenium WebDriver set-up
    service = Service("chromedriver.exe")  # Place chromedriver.exe in code folder else replace with system path of chromedriver
    driver = webdriver.Chrome(service=service)

    try:
        #Open GoogleMaps and search for the given purpose
        driver.get("https://www.google.com/maps")
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(purpose)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        #Scrol and Results fetch variables
        action = ActionChains(driver)
        scroll_pause_time = 2
        results = driver.find_elements(By.CLASS_NAME, "hfpxzc")
        le = 0  #Counter to detect scroll stuck

        # Scrolls till limit or all results are loaded
        while (limit is None or len(results) < limit) and le <= 20:
            print(f"Current results: {len(results)}")
            prev_len = len(results)

            #Scroll down to load more results
            if results:
                scroll_origin = ScrollOrigin.from_element(results[-1])
                action.scroll_from_origin(scroll_origin, 0, 1000).perform()
                time.sleep(scroll_pause_time)

            results = driver.find_elements(By.CLASS_NAME, "hfpxzc")

            #Check if scrolling stopped or not
            if len(results) == prev_len:
                le += 1
            else:
                le = 0

        #List to store all extracted businesses
        businesses = []

        #Iterate over each result and extract data
        for i, result in enumerate(results):
            if limit and i >= limit:
                break

            try:
                #Click on each of the results to load more details
                action.move_to_element(result).perform()
                result.click()
                #Change this to configure how long you want to wait before selecting the next result // Increase value if internest speed is low hehe!!
                time.sleep(5)

                #Parse the page source with BeautifulSoup
                soup = BeautifulSoup(driver.page_source, "html.parser")

                #Extract details
                name_tag = soup.find("h1", {"class": "DUwDvf lfPIob"})
                name = name_tag.text if name_tag else "No name"

                info_tags = soup.find_all("div", {"class": "Io6YTe fontBodyMedium kR99db fdkmkc"})

                phone = info_tags[2].text if (len(info_tags) > 2 and info_tags[2].text.strip().startswith("0")) else "No phone"
                address = info_tags[0].text if len(info_tags) > 0 else "No address"
                raw_website = info_tags[1].text.strip() if len(info_tags) > 1 else ""
                website = raw_website if is_valid_website(raw_website) else "No website"

                #Append the data to the businesses list
                businesses.append({
                    "Name": name,
                    "Phone": phone,
                    "Address": address,
                    "Website": website,
                })

                #Save data to a CSV file after each business
                pd.DataFrame(businesses).to_csv(purpose+".csv", index=False)

                print(f"Scraped: {name}, {phone}, {address}, {website}")

            except Exception as e:
                print("Error while processing a result:", e)
                continue

    finally:
        #Close the WebDriver
        driver.quit()

    print("Scraping completed. Data saved to "+purpose+".csv.")

#Specify a limit or leave it as None to scrape all available results
# scrape_travel_companies(limit=10)
scrape_travel_companies()
