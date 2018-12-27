import requests, sys, time
import urllib.request
from bs4 import BeautifulSoup

class downloader(object):
    def __init__(self):
        self.server = 'https://www.biqukan.com/'
        self.target = ''  #'https://www.biqukan.com/56_56384/'
        self.title = ''
        self.names = []
        self.urls = []
        self.nums = 0
    
    def searchNovel(self):
        content = input('Please input the novel title: ')
        self.title = content
        content += ' www.biqukan.com'
        contentCode  = urllib.request.quote(content)
        url = 'http://www.baidu.com/s?wd=' + contentCode
        # print('内容搜索地址:'+url)

        print('Current server: '+self.server)
        print('Searching...')
        req = requests.get(url = url)
        html = req.text
        div_bf = BeautifulSoup(html, features='html.parser')
        div = div_bf.find_all('div', class_='result c-container ', id='1')
        bf = BeautifulSoup(str(div[0]), features='html.parser')
        texts = bf.find_all('a')
        url2 = texts[0].get('href') 
        # print('搜索结果地址：'+url2)

        response = requests.get(url = url2)
        realURL = response.url
        # print('The real URL is: ' + realURL)
    
        self.target=realURL     

    def getDownloadUrl(self):
        req = requests.get(url = self.target)
        html = req.text
        div_bf = BeautifulSoup(html,features='html.parser')
        div = div_bf.find_all('div', class_='listmain')
        a_bf = BeautifulSoup(str(div[0]),features='html.parser')
        a = a_bf.find_all('a')
        self.nums = len(a[12:])
        for each in a[12:]:
            self.names.append(each.string)
            self.urls.append(self.server+each.get('href'))

    def getContents(self, target):
        req = requests.get(url = target)
        html = req.text
        bf = BeautifulSoup(html,features='html.parser')
        texts = bf.find_all('div', class_='showtxt')
        # print(len(texts))
        texts = texts[0].text.replace('\xa0'*8, '\n\n')
        return texts

    def writer(self, name, path, text):
        writeFlag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


dl = downloader()
dl.searchNovel()
dl.getDownloadUrl()
open(dl.title+'.txt', 'w', encoding='utf-8')
print('Downloading...')
for i in range(dl.nums):
    dl.writer(dl.names[i], dl.title+'.txt', dl.getContents(dl.urls[i]))
    sys.stdout.write('                                                                         \r')
    sys.stdout.write(dl.names[i] + '......' + "Completed:%.3f%%" % float((i+1)/dl.nums*100) + '\r')
    sys.stdout.flush()
    time.sleep(10)  #防止网站反扒
print()
print('Finished!')