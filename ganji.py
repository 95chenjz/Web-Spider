import requests
from bs4 import BeautifulSoup
import codecs

def get_html(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = 'utf-8'#r.apparent_encoding()
        return r.text

    except:
        return 'ERROR1'


def get_contents(target):
    """

    :param self:
    :param target:
    :return:
    """
    req = requests.get(url = target)
    html = req.text
    bf = BeautifulSoup(html, 'lxml')

    content = {}
    content['title'] = bf.title.text.strip()
    table = bf.find_all('td')
    content['price'] = table[0].contents[0].text.strip()
    content['area'] = table[1].contents[1].text.strip()
    content['orig'] = table[2].contents[0].strip()

    content['tel'] = bf.find_all('div', class_='tel-area radius')[0].contents[1].text.strip()

    return content

def main(base_url, num):
    url_list = [base_url]

    for i in range(0, num):
        url_list.append(base_url + '?page=2&url=shoucangpin&pageSize=10&deal_type=1&agent=1&ifid=gj3g_list_next_wu')
    print('Spider awaken')

    for i in url_list:
        contents = get_contents(i)
    print(contents)
    print('Finish')

base_url =    'https://3g.ganji.com/bj_shoucangpin/3444906820x?pos=1&page=3&tg=&url=shoucangpin&pageSize=10&deal_type=1&agent=1'
#'https://3g.ganji.com/bj_shoucangpin/'

if __name__ == '__main__':
    contents = main(base_url,3)
    print(contents)
