import requests, sys, time
from bs4 import BeautifulSoup

class downloader(object):
    def __init__(self):
        self.server = 'https://www.biqukan.com/'
        self.target = 'https://www.biqukan.com/56_56384/'
        self.names = []
        self.urls = []
        self.nums = 0

    def getDownloadUrl(self):
        req = requests.get(url = self.target)
        html = req.text
        div_bf = BeautifulSoup(html,features='html.parser')
        div = div_bf.find_all('div', class_='listmain')
        a_bf = BeautifulSoup(str(div[0]),features='html.parser')
        a = a_bf.find_all('a')
        self.nums = len(a[12:200])
        for each in a[12:200]:
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
dl.getDownloadUrl()
print('Downloading...')
for i in range(dl.nums):
    dl.writer(dl.names[i], '大龟甲师.txt', dl.getContents(dl.urls[i]))
    sys.stdout.write('                                                                         \r')
    sys.stdout.write(dl.names[i] + '......' + "Completed:%.3f%%" % float((i+1)/dl.nums*100) + '\r')
    sys.stdout.flush()
    time.sleep(10)  #防止网站反扒
print('Finished!')