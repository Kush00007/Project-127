from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

browser = webdriver.Chrome("E:/WhiteHatProjects/C127-Web-scraping-1/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)
planets_data = []

# Define Exoplanet Data Scrapping Method
def scrape():

    for i in range(0,10):
        print(f'Scrapping page {i+1} ...' )
                ## ADD CODE HERE ##
        soup = BeautifulSoup(browser.page_source, "html.parser")

        for ul_tag in soup.find_all("ul", attrs = {"class","exoplanet"}):
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
        browser.find_elemt(by = By.XPATH, value ='/html/body/div[3]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/section/div/div/div/ul[2]' )


        
# Calling Method    
scrape()

# Define Header
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]

# Define pandas DataFrame   
planet_df_1 = pd.DataFrame(planets_data, columns = headers)

# Convert to CSV
planet_df_1.to_csv('scraped_data.csv',index = True, index_label = 'id')
    
