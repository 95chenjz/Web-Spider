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

def get_content(url):
    """
    Analyze html, save comments and more information
    :param url: link of the BBS
    :return: a dictionary of comments
    """

    comments = [] # a list of 帖子

    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')

    liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})

    for i in liTags:
        comment = {}

        try:
            comment['title'] = i.find('a', attrs={'class':'j_th_tit '}).text.strip()
            comment['link'] = 'http://tieba.baidu.com/' + i.find('a', attrs={'class':'j_th_tit '})['href']
            comment['name'] = i.find('span', attrs={'class':'tb_icon_author '}).text.strip()
            comment['time'] = i.find('span',attrs={'class': 'pull-right is_show_create_time'}).text.strip()
            comment['replyNum'] = i.find('span', attrs={'class','threadlist_rep_num center_text'}).text.strip()
            comments.append(comment)

        except:
            print("Error2")

    return comments

def Out2File(dict):
    """
    write to local file TTBT.txt
    :param dict: comments
    """
    with codecs.open('TTBT.txt', 'a+', encoding='utf-8') as f:
        for comment in dict:
            f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量： {} \n'.format(
                comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))

        print('Finish')

def main(base_url, deep):
    url_list = []

    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50 * i))
    print('所有的网页已经下载到本地！ 开始筛选信息')

    for i in url_list:
        content = get_content(i)
        # print(content)
        Out2File(content)
    print('所有的信息都已经保存完毕！')

base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'
# 设置需要爬取的页码数量
deep = 3

if __name__ == '__main__':
    main(base_url, deep)