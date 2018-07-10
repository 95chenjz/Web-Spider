from bs4 import BeautifulSoup
import requests, sys

class downloader(object):

    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.target = 'http://www.biqukan.com/1_1094/'
        self.names = [] # names of chapters
        self.urls = []  # links of chapters
        self.nums = 0   # number of chapters

    def get_down_url(self):
        """
        for links
        :return:
        None
        """
        req = requests.get(url = self.target)
        html = req.text
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('div', class_ = 'listmain')
        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[15:]) # delete unnecessary
        for i in a[15:]:
            self.names.append(i.string)
            self.urls.append(self.server + i.get('href'))

    def get_contents(self, target):
        """
        gete contents
        :param self:
        :param target: target url
        :return: texts
        """
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('div', class_ = 'showtxt')
        texts = texts[0].text.replace('\xa0'*8, '\n\n')
        return texts

    def writer(self, name, path, text):
        writer_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')

if __name__ == '__main__':
    dl = downloader()
    dl.get_down_url()
    print('开始下载：；')
    for i in range(dl.nums):
        dl.writer(dl.names[i], 'function.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write('  已下载：%.3f%%' % float(i/dl.nums * 100) + '\r')
        sys.stdout.flush()

    print('下载完成')