from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd

START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

service = Service(executable_path='./chromedriver.exe')
browser = webdriver.Chrome(service=service)
browser.get(START_URL)

time.sleep(10)
planets_data = []

# Define Exoplanet Data Scraping Method
def scrape():
    for i in range(0, 10):
        print(f'Scraping page {i + 1} ...')
        soup = BeautifulSoup(browser.page_source, "html.parser")

        for ul_tag in soup.find_all("ul", attrs={"class": "exoplanet"}):
            li_tags = ul_tag.find_all("li")

            temp_list = []

            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            planets_data.append(temp_list)

        # Navigate to the next page
        next_button = browser.find_element(By.XPATH, '//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a')
        next_button.click()
        time.sleep(5)  # Wait for the page to load

# Calling Method
scrape()

# Define Header
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]

# Define pandas DataFrame
planet_df_1 = pd.DataFrame(planets_data, columns=headers)

# Convert to CSV
planet_df_1.to_csv('scraped_data.csv', index=True, index_label='id')

browser.quit()
