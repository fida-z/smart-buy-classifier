from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time


def fetch_similar(model_name):
    # Setup headless Firefox options required for Streamlit Cloud servers
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)

    def get_listing_urls(model_name, max_listings=5):

        slug = model_name.lower().replace(" ", "-")
        search_url = (f"https://www.cardekho.com/used-{slug}+cars+in+new-delhi")
        driver.get(search_url)
        print('Searching...')
        print("Requested URL:", search_url)
        print("Actual URL:", driver.current_url)
        print("Page title:", driver.title)
        urls = set()
        last_height = 0

        while len(urls) < max_listings:
            for _ in range(5):
                driver.execute_script("window.scrollBy(0, 2000);")
                time.sleep(0.5)

            links = driver.find_elements(By.XPATH,"//div[contains(@class,'titlebox')]//h3/a")
            for link in links:
                href = link.get_attribute("href")
                print('Getting URLs')
                if href:
                    urls.add(href)
                if len(urls) >= max_listings:
                    break

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        return list(urls)

    def get_car_data(url_list):
        for url in url_list:
            try:
                driver.get(url)
                wait = WebDriverWait(driver, 20)
                print('On a page')
                
                model_element = wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
                price_element = wait.until(EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "price")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'price')]"))
                    ))
                owner_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'specs')]")))

                # refining:
                p_text = price_element.text.replace('\n',' ').split(' ')[:4]
                mkt_type = (' ').join(p_text[0:2])
                price = (' ').join(p_text[2:])

                o_text = owner_element.text.replace('\n·\n',' ').split(' ')
                km_driven = (' ').join(o_text[:2])
                owner = (' ').join(o_text[-2:])

                yield {
                    "Link": url,
                    "Model": model_element.text,
                    "Price": price,
                    'Market Value': mkt_type,
                    'KM Driven': km_driven,
                    'Owner': owner
                }
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                continue

    try:
        urls = get_listing_urls(model_name)
        print('Sending to Streamlit')
        for listing in get_car_data(urls):
            yield listing
    finally:
        driver.quit()

