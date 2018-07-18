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

def get_links(url):

    links = []

    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    aTags = soup.find_all('a', attrs={'class':'infor'})

    for i in aTags:
        try:
            link = 'http://3g.ganji.com/' + i['href']
            #print(link)
            links.append(link)

        except:
            print('Error1')

    return links

def get_contents(link_url):

    html = get_html(link_url)
    soup = BeautifulSoup(html, 'lxml')

    content = {}

    try:
        content['title'] = soup.title.text.strip()
        table = soup.find_all('td')
        content['price'] = table[0].contents[0].text.strip()
        try:
            content['area'] = table[1].contents[1].text.strip()
            content['orig'] = table[2].contents[0].strip()
        except:
            content['area'] = 'NA'
            content['orig'] = 'NA'
        content['tel'] = soup.find_all('div', class_='tel-area radius')[0].contents[1].text.strip()

    except:
        print()

    return content

def Out2File(contents:dict):

    with codecs.open('BeijingGanji.csv', 'w', encoding='utf-8') as f:
#        f.write(codecs.BOM_UTF8)
        f.write('title, price, area, orig, tel\n')
        for content in contents:
            f.write('{}, {}, {}, {}, {}\n'.format(content['title'], content['price'], content['area'], content['orig'], content['tel']))

        f.close()


def main(page_num):
    contents = []
    for i in range(1, page_num+1):
        url = 'https://3g.ganji.com/bj_shoucangpin/?page={}&url=shoucangpin&pageSize=10&deal_type=1&agent=1&ifid=gj3g_list_next_wu'.format(i)
        links = get_links(url)
        for link in links:
            contents.append(get_contents(link))
    Out2File(contents)
            #print(contents)
            #print('=============')

if __name__ == '__main__':
    main(5)
# url = 'https://3g.ganji.com/bj_shoucangpin/?page=2&url=shoucangpin&pageSize=10&deal_type=1&agent=1&ifid=gj3g_list_next_wu'
# links = get_links(url)
# for link in links:
#     print(link)
#     print(get_contents(link))