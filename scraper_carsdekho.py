import bs4
import requests
import random
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# fetching the page containing urls:


driver = webdriver.Firefox()
driver.maximize_window()
driver.get('https://www.cardekho.com/used-cars+0-lakh-to-1-lakh+in+delhi-ncr')
urls = set()
last_height = 0



while True:
    for i in range(20): 
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(1)    
        
    time.sleep(2)

    links = driver.find_elements(By.XPATH, "//div[@class='titlebox']/h3/a")
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
    with open('cardekho.txt','a', encoding='utf-8') as wf:
        for url in url_list:
            try:
                data = {}



                wait = WebDriverWait(driver,20)
                driver.get(url)
                model = wait.until(EC.presence_of_element_located((By.XPATH, "//h1"))).text
                price = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='vehiclePrice']/span"))).text   
                price_score = 'NA'
                plate = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.outer-card-container:nth-child(5) > ul:nth-child(2) > li:nth-child(6) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)'))).text
                reg_year = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.outer-card-container:nth-child(5) > ul:nth-child(2) > li:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)'))).text
                fuel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.outer-card-container:nth-child(5) > ul:nth-child(2) > li:nth-child(3) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)'))).text
                km_driven = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.outer-card-container:nth-child(5) > ul:nth-child(2) > li:nth-child(5) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)'))).text
                transmission = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'li.gsc_col-xs-12:nth-child(9) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)'))).text
                engine_capacity = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.outer-card-container:nth-child(7) > ul:nth-child(2) > li:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)'))).text
                ownership = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'li.gsc_col-xs-12:nth-child(7) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)'))).text
                make_year = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'li.gsc_col-xs-12:nth-child(10) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)'))).text
                insurance =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.outer-card-container:nth-child(5) > ul:nth-child(2) > li:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)'))).text
                


                data['model'] = model
                data['price'] = price
                data['price_score'] = price_score
                data['plate'] = plate
                data['Reg. Year'] = reg_year
                data['Fuel'] = fuel
                data['KM Driven'] = km_driven
                data['Transmission'] = transmission
                data['Engine capacity'] = engine_capacity
                data['Ownership'] = ownership
                data['Make year'] = make_year
                data['Insurance type'] = insurance
                


                
                wf.write(f"{data}\n")
                wf.flush()
                time.sleep(random.uniform(3,5))



            except Exception as e:
                print(f"Error fetching {url} because {e}")

get_car_data(urls)
driver.close()