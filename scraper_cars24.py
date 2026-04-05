import bs4
import requests
import random
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import xml.etree.ElementTree as ET


# fetching the page containing xml:

website = requests.get('https://www.cars24.com/sitemaps/buy-used-cars-new-delhi.xml').text
bs = bs4.BeautifulSoup(website, 'xml').prettify()

# parsing the xml to obtain urls:

tree = ET.parse('smart-buy-classifier\cars24delhi.xml')
root = tree.getroot()

urls = []
for url in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
    urls.append(str(url.text).strip())


driver = webdriver.Firefox()

urls_sub1 = urls[:1000]
urls_sub2 = urls[1000:2000]
urls_sub3 = urls[2000:3000]
urls_sub4 = urls[3000:4000]
urls_sub5 = urls[4000:]

with open('data.txt','a', encoding='utf-8') as wf:
    for url in urls_sub1:
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
            print(f"Error fetching {url} becuase {e}")


driver.close()