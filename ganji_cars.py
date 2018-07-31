import requests
from bs4 import BeautifulSoup
import codecs
from selenium import webdriver
import time
import re

def contents_url(url):
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    browser = webdriver.Chrome()
    browser.get(url)

    browser.find_element_by_class_name('detail_tel_400_outer').click()
    time.sleep(1)
    html = browser.page_source

    return(html)

def get_html(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = 'utf-8'#r.apparent_encoding()
        return r.text

    except:
        return 'ERROR1'

def get_contents(url):

    html = contents_url(url)
    soup = BeautifulSoup(html, 'lxml')

    contents = {}


    try:
        contents['title'] = soup.title.text.strip()
        contents['tel'] = soup.find_all('div', class_='detail_tel_400_text click_change_div')[0].contents[0]
        ppl = soup.find_all('p', class_='v-p2')[0].contents[1].strip()
        ppl = re.sub(' ', '', ppl)
        contents['ppl'] = ppl
        price = soup.find_all('span', class_='sp')[0].contents[0].contents[0] + \
                soup.find_all('span', class_='sp')[0].contents[1]
        contents['price'] = price

    except:
        print('ERROR2')

def get_links(base_url):

    html = get_html(base_url)
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)

    tags = soup.find_all('a', class_='infor-title pt_tit js-title')

    if tags is None:
        return tags
    links = []

    for link in tags:
        # print(link['href'])
        links.append(link)

    return links

get_urls('http://bj.ganji.com/ershouche/a1b25e999/')
