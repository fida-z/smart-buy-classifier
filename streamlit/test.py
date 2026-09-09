
import bs4
import requests
import random
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def fetch_similar(model_name):
    def listing_url(model):
        slug = model.lower().replace(" ", "-")
        return f"https://www.cardekho.com/used-{slug}+cars+in+delhi-ncr"


    def get_car_data(url_list):
            cardata = []
            for url in url_list:
                try:
                    data = {}

                    wait = WebDriverWait(driver,20)
                    driver.get(url)
                    model = wait.until(EC.presence_of_element_located((By.XPATH, "//h1"))).text
                    price = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='vehiclePrice']/span"))).text  
                    fuel = wait.until(EC.presence_of_element_located((By.XPATH,"//div[normalize-space()='Fuel Type']/following-sibling::span"))).text
                    km_driven = wait.until(EC.presence_of_element_located((By.XPATH,"//div[normalize-space()='Kms Driven']/following-sibling::span"))).text
                    transmission = wait.until(EC.presence_of_element_located((By.XPATH,"//div[normalize-space()='Transmission']/following-sibling::span"))).text
                    engine_capacity = wait.until(EC.presence_of_element_located((By.XPATH,"//div[normalize-space()='Engine Displacement']/following-sibling::span"))).text
                    ownership = wait.until(EC.presence_of_element_located((By.XPATH,"//div[normalize-space()='Ownership']/following-sibling::span"))).text
                    


                    data['model'] = model
                    data['price'] = price
                    data['Fuel'] = fuel
                    data['KM driven'] = km_driven
                    data['Transmission'] = transmission
                    data['Engine capacity'] = engine_capacity
                    data['Ownership'] = ownership
                    cardata.append(data)

                    time.sleep(random.uniform(3,5))



                except Exception as e:
                    print(f"Error fetching {url} because {e}")
            return(cardata)



    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(listing_url(model_name))
    urls = set()


    driver.execute_script("window.scrollBy(0, 2000);")            
    time.sleep(2)

    links = driver.find_elements(By.XPATH, "//div[contains(@class,'titlebox')]//h3/a")
    for link in links:
        href = link.get_attribute('href')
        if href:
            urls.add(href)
        
    cardata = get_car_data(urls)
    driver.close()

    return(cardata)
  


fetch_similar('HONDA CITY')