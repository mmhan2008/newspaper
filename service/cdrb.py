# -*- coding: utf-8 -*-
import time
import random
import requests
from bs4 import BeautifulSoup

from util.LoggerClass import Logger
from util.configutil import getconfig

logger = Logger(logname= 'newspaper',logger='cdrb').getlog()

def parse_url():
    list = []
    tempurl = formatUrl()
    flag = True
    i = 0
    try:
        while flag:
            i += 1
            str = "%02d"%i
            url = tempurl.format(str)
            # print(url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
            resp = requests.get(url, headers=headers, timeout=10)
            resp.encoding = resp.apparent_encoding
            html = resp.text
            if resp.status_code == 200:
                soup = BeautifulSoup(html, 'html.parser')
                div = soup.find('div',attrs={'class':'news-list'})
                for link in div.find_all('a'):
                    path = link.get('href')
                    title = link.get_text().strip()
                    if title == '':
                        pass
                    else:
                        resp1 = requests.get(path, headers=headers, timeout=10)
                        resp1.encoding = resp1.apparent_encoding
                        if resp1.status_code == 200:
                            resource = resp1.text
                            bsoup = BeautifulSoup(resource, 'html.parser')
                            nohtml_content = bsoup.find('founder-content').get_text().strip()
                            content = bsoup.find('founder-content').find_all('p')
                            list.append('{}###{}###成都日报###{}###{}'.format(path,title,nohtml_content,content))
                        time.sleep(random.randint(0,2))
            else:
                flag = False
    except Exception as e:
        logger.info('=========================成都日报解析异常=========================')
        logger.info(url)
        logger.info(e)
    finally:
        return list


def formatUrl():
    url = getconfig('urls','cdrb')
    date = time.strftime('%Y%m/%d',time.localtime(time.time()))
    formatUrl = url.format(date,'{}')
    return formatUrl

if __name__ == '__main__':
    list =  parse_url()
    for str in list:
        print(str)
    print(list.__len__())