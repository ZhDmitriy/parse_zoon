from email import header
from bs4 import BeautifulSoup as bs 
import requests
import csv
from itertools import dropwhile
from lib2to3.pgen2 import driver
from operator import delitem, imod
from re import I
from selenium.webdriver.common.keys import Keys
from stringprep import in_table_a1
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import lxml
import json
import socket

headers = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
}

user_agent = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36", 
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36", 
    "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36", 
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
]

option = webdriver.ChromeOptions()
option.add_argument(f"user-agent={random.choice(user_agent)}")

driver = webdriver.Chrome(executable_path="C:\\Users\\Shhhn\\OneDrive\\Рабочий стол\\web_menu\\selenium_parser\\chromedriver_win32\\chromedriver.exe", options=option)
url = "https://kazan.zoon.ru/beauty/"
driver.get(url=url)

def scroll(): 
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(3)
        if lastCount==lenOfPage:
            match=True

scroll()

time.sleep(3)
with open("C:\\Users\\Shhhn\\OneDrive\\Рабочий стол\\web_menu\\selenium_parser\\parser.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

with open("C:\\Users\\Shhhn\\OneDrive\\Рабочий стол\\web_menu\\selenium_parser\\parser.html", "r", encoding="utf-8") as file:
    src = file.read()
        
soup = bs(src, "lxml")
items_urls = soup.find_all("a", class_='title-link js-item-url')

urls = []
for item in items_urls:
    urls.append(item['href'])

with open("C:\\Users\\Shhhn\\OneDrive\\Рабочий стол\\web_menu\\selenium_parser\\urls.txt", "w", encoding="utf-8") as file:
    for url_ in urls:
        file.write(f"{url_}\n")

#обработка ссылок
# with open("C:\\Users\\Shhhn\\OneDrive\\Рабочий стол\\web_menu\\selenium_parser\\urls.txt", "r", encoding="utf-8") as file:
#     urls_list = file.readlines

result_list = []
count = 0

for url in urls:
    response = requests.get(url=url, headers=headers, timeout=5)
    soup = bs(response.text, "lxml")
    
    try:
        item_name = soup.find("span", {"itemprop":"name"}).text.strip()
    except Exception as _error:
        item_name = None 
        
    item_phones_list = []
    try:
        item_phones = soup.find("div", {"class":"service-phones-box"}).find("div", {"class":"service-phones-list"}).find_all("a", {"class":"tel-phone js-phone-number"})
        for phone in item_phones:
            item_phone = phone["href"].split(":")[-1]
            item_phones_list.append(item_phone)
    except Exception as _error:
        item_phones_list = "Emty"
    
    result_list.append(
        {
            "Name": item_name, 
            "Link": url, 
            "Phones":item_phones_list
        }
    )
    
    time.sleep(random.randrange(1,4))
    if count%10 == 0:
        time.sleep(random.randrange(3,6))
    count+=1
    print(f"Обработано: {count} ссылок")
    
    # if count == 10:
    #     break
#обработка ссылок

with open("C:\\Users\\Shhhn\\OneDrive\\Рабочий стол\\web_menu\\selenium_parser\\result.json", "w", encoding="utf-8") as file:
    json.dump(result_list, file, indent=4, ensure_ascii=False)

print("OK")
time.sleep(5)
driver.close()
driver.quit()



