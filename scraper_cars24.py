import bs4
import requests
import random
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import xml.etree.ElementTree as ET


# fetching the page containing urls:


driver = webdriver.Firefox()
driver.maximize_window()
driver.get('https://www.cars24.com/buy-used-cars-delhi-ncr/?sort=lhl&serveWarrantyCount=true&listingSource=ViewAllCars&storeCityId=2')
urls = set()
last_height = 0


while True:
    for i in range(20): 
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(1)    
        
    time.sleep(2)

    links = driver.find_elements(By.CSS_SELECTOR, 'a.styles_carCardWrapper__sXLIp')
    for link in links:
        href = link.get_attribute('href')
        if href:
            urls.add(href)
    
    new_height = driver.execute_script('return document.body.scrollHeight')

    if(new_height == last_height):
        break
    else:
        last_height = new_height
        print(f"Captured {len(urls)} unique URLs so far...")





def get_car_data(url_list):
    with open('data.txt','a', encoding='utf-8') as wf:
        for url in url_list:
            try:
                data = {}

                wait = WebDriverWait(driver,20)
                driver.get(url)
                model = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
                price = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "lfZZUB"))).text    
                price_score = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "styles_information__Y5fPZ"))).text
                plate_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'styles_carMeta__hm1XQ')))
                plate = plate_container.find_elements(By.TAG_NAME, 'p')[-1].text
                
                info_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "styles_content__KtXDs")))
                infos = info_container.find_elements(By.TAG_NAME, 'li')
                specs_dict = {}
                
                for info in infos:
                    para = info.find_elements(By.TAG_NAME, 'p')
                    label = para[0].text.strip()
                    value = para[1].text.strip()
                    specs_dict[label] = value

                data['model'] = model
                data['price'] = price
                data['price_score'] = price_score
                data['plate'] = plate
                data['info'] = specs_dict

                
                wf.write(f"{data}\n")
                wf.flush()
                time.sleep(random.uniform(3,7))



            except Exception as e:
                print(f"Error fetching {url} because {e}")

get_car_data(urls)
driver.close()