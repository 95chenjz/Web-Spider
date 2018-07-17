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

def get_comments(url):
    """
    >>> get_comments('https://tieba.baidu.com/p/4243062672?fr=ala0&pstaala=1&tpl=5&fid=8519820&isgod=0&red_tag=0519724203')

    """
    comments = []

    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    cons = soup.find_all('div', attrs={'class':'d_post_content j_d_post_content '})
    for con in cons:
        comments.append(con.text.strip())

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

    words = []
    links = []
    for i in url_list:
        content = get_content(i)
        #Out2File(content)

    for i in content:
        words.append(['title'])
        links.append(i['link'])

    with codecs.open('JDAuction.txt', 'a+', encoding='utf-8') as f:
        for i in links:
            content2 = get_comments(i)
         #   print(content2)
            f.write('{}\n'.format(content2))


    #print(words)
    print('所有的信息都已经保存完毕！')

#生活大爆炸
#base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'

#京东拍卖
base_url = 'https://tieba.baidu.com/f?kw=%BE%A9%B6%AB%C5%C4%C2%F4&fr=ala0&tpl=5'
# 设置需要爬取的页码数量
deep = 1

if __name__ == '__main__':
    main(base_url, deep)