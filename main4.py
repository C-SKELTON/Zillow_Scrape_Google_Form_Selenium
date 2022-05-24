import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

google_form = 'https://docs.google.com/forms/d/e/1FAIpQLSf7t7rpoYgjvDYnUYIEWocv_abJJFYikShVJCT9vutpO5Mzyw/viewform?usp=sf_link'
zillow_link = 'https://www.zillow.com/san-francisco-ca/rent-houses-1-bedrooms/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-123.54432193164062%2C%22east%22%3A-121.32233706835937%2C%22south%22%3A36.86447819404016%2C%22north%22%3A38.67502148593923%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22beds%22%3A%7B%22min%22%3A1%2C%22max%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A4000%7D%2C%22price%22%3A%7B%22max%22%3A937268%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A9%7D'

headers = {
    "Accept-Language":"en-US,en;q=0.9",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
}
chrome_driver_path = Service("C:/Users/conno/chrome_driver/chromedriver")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=chrome_driver_path, options=op)
time.sleep(5)


r = requests.get(zillow_link, headers=headers)
zillow_results = r.text
soup = BeautifulSoup(zillow_results, "html.parser")

data = json.loads(
    soup.select_one("script[data-zrr-shared-data-key]")
        .contents[0]
        .strip("!<>-")
)


# get house links
house_links = [
    x["detailUrl"]
    for x in data["cat1"]["searchResults"]["listResults"]
]

# amend house_links to have all proper URLS
house_links = [
    link.replace(link, "https://www.zillow.com" + link)
    if not link.startswith("http")
    else link
    for link in house_links
]

# Get address
house_address = [
    result["address"]
    for result in data["cat1"]["searchResults"]["listResults"]
]

# Get price
house_rent = [
    int(result["units"][0]["price"].strip("$").replace(",", "").strip("+"))
    if "units" in result
    else result["unformattedPrice"]
    for result in data["cat1"]["searchResults"]["listResults"]

]

driver.get(google_form)

time.sleep(5)
for a in range(len(house_links)):
    addr_input = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    prop_link = driver.find_element(By.XPATH,
                                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    addr_input.send_keys(house_address[a])
    price_input.send_keys(house_rent[a])
    prop_link.send_keys(house_links[a])
    time.sleep(2)
    btn.click()
    time.sleep(3)
    click_agn = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    click_agn.click()
    time.sleep(3)


