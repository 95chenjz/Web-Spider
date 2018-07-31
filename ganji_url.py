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
        try:
            content['title'] = soup.title.text.strip()
        except:
            content['title'] = 'NA'
        table = soup.find_all('td')
        try:
            content['price'] = table[0].contents[0].text.strip()
        except:
            content['price'] = 'NA'
        try:
            content['area'] = table[1].contents[1].text.strip()
            content['orig'] = table[2].contents[0].strip()
        except:
            content['area'] = 'NA'
            content['orig'] = 'NA'
        try:
            content['tel'] = soup.find_all('div', class_='tel-area radius')[0].contents[1].text.strip()
        except:
            content['tel'] = 'NA'
    except:
        print()

    return content


def Out2File(contents:dict):

    with codecs.open('Ganji_shoucang.csv', 'a', encoding='utf-8') as f:
#        f.write(codecs.BOM_UTF8)
        f.write('title, price, area, orig, tel\n')
        for content in contents:
            f.write('{}, {}, {}, {}, {}\n'.format(content['title'], content['price'], content['area'], content['orig'], content['tel']))
        f.close()


def main(page_num, loc):

    for i, j in zip(page_num, loc):
        contents = []
        for n in range(1, i+1):
            url = 'https://3g.ganji.com/{}_shoucangpin/?page={}&url=shoucangpin&pageSize=10&deal_type=1&agent=1&ifid=gj3g_list_next_wu'.format(j, n)
            links = get_links(url)
            for link in links:
                contents.append(get_contents(link))
        Out2File(contents)
            #print(contents)
            #print('=============')
        print(j, ' finish')
if __name__ == '__main__':
    page = [129, 20, 16, 13, 46, 54, 20, 16, 15, 12, 29]
    loc = ['hrb', 'hz', 'nb', 'xm', 'sy', 'dg', 'cc', 'cs', 'ty', 'nn', 'sjz']

    # 'bj', 'gz', 'sh', 'tj', 'sz', 'cq', 'nj', 'wh','cd', 'xa', 'zz', 'dl', 'sz', 'jn', 'qd',
    # 139, 111, 47, 80, 76, 95, 36, 57, 65, 48, 25, 35, 76, 54, 90,
    main(page, loc)
#      139, 111, 47, 80, 76, 95, 36, 57, 65, 48, 25, 35, 76, 54, 90, 129, 20, 16, 13, 46, 54, 20, 16, 15, 12, 29
#       bj, gz, sh, tj, sz, cq, nj, wh, cd, xa, zz, dl, sz, jn, qd, hrb, hz, nb, xm, sy, dg, cc, cs, ty, nn, sjz
# url = 'https://3g.ganji.com/bj_shoucangpin/?page=2&url=shoucangpin&pageSize=10&deal_type=1&agent=1&ifid=gj3g_list_next_wu'



    # 北京    广州    上海    天津    深圳    重庆    南京    武汉    成都    西安    郑州    大连    苏州    济南    青岛
    # 哈尔滨    杭州    宁波    厦门    沈阳    东莞    长春    长沙      太原       南宁    石家庄

