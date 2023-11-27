import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# web-scraping beautiful soup

def webscrape_bs(url_, params_):
    response = requests.get(url=url_, params=params_)
    if response.status_code == 200:
        print('Request is successful')
        soup = BeautifulSoup(response.content, 'html.parser')
        post_titles = soup.find_all('h2', class_='post-title')
        for title in post_titles:
            print(title.text.strip())
    else:
        print('Response status code is not 200')


# web-scraping with selenium

def webscrape_selenium_search_product(url_, params_, driver_path_, product_name_):
    driver = webdriver.Safari()
    driver.get(url_)
    search_box = driver.find_element(By.ID, "ProductInfo-8574337089823")
    search_box.send_keys(product_name_)
    search_box.send_keys(Keys.ENTER)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
    element_text = element.text
    print(element_text)
    all_products = driver.find_elements(By.CLASS_NAME, 'product_card')
    print(f'There are {len(all_products)} {product_name_}s on the page.')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    driver.save_screenshot("screenshot.png")
    driver.quit()


url = 'https://blog.apify.com/'
params = {'Content-Type': 'plain/text'}
webscrape_bs(url, params)
selenium_url = 'https://www.montypythononlinestore.com/'
selenium_params = {'Content-Type': 'plain/text'}
driver_path = '/usr/local/bin/safaridriver'
webscrape_selenium_search_product(selenium_url, params, driver_path, product_name_='t-shirt')
