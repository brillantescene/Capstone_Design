import requests
from selenium import webdriver
from bs4 import BeautifulSoup


def freesound_pages(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    paginator = soup.find("div", {"class": "search_paginator"})
    links = paginator.find_all("a")
    pages = []
    for link in links[1:]:
        pages.append(int(link.string))
    last_page = pages[-1]
    return last_page


def extract_links(last_page, URL):
    links = []
    for page in range(1, last_page+1):
        result = requests.get(f"{URL}&page={page}#sound")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "sound_filename"})
        for result in results:
            links.append(result.find("a")["href"])
    return links


driver = webdriver.Chrome('/Users/park-yujin/Downloads/chromedriver')
driver.implicitly_wait(3)
driver.get('https://freesound.org/home/login')
driver.find_element_by_name('username').send_keys('glisteneugene')
driver.find_element_by_name('password').send_keys('cherishDaniel97!')
driver.find_element_by_xpath('//*[@id="content_full"]/form/input[2]').click()


categories = ["vacuum+cleaner", "glass+breaking"]

for category in categories:
    URL = f"https://freesound.org/search/?q={category}"
    last_page = freesound_pages(URL)
    links = extract_links(last_page, URL)
    for link in links:
        driver.get(f"https://freesound.org{link}")
        result = driver.page_source
        soup = BeautifulSoup(result, "html.parser")
        download = soup.find_all("div", id="download")
        for dl in download:
            download_link = dl.find("a")["href"]
            driver.get(f"https://freesound.org{download_link}")
            print(f"[{category}]__{download_link} is done!")
