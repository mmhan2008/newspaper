# -*- coding: utf-8 -*-
import time
from urllib import parse
import random
import requests
from bs4 import BeautifulSoup

from util.LoggerClass import Logger
from util.configutil import getconfig

logger = Logger(logname= 'newspaper',logger='dlrb').getlog()

def parse_url():
    list = []
    tempurl = formatUrl()
    flag = True
    i = 1
    try:
        while flag:
            i += 1
            url = tempurl.format(i)
            # print(url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
            resp = requests.get(url, headers=headers, timeout=10)
            resp.encoding = resp.apparent_encoding
            html = resp.text
            if resp.status_code == 200:
                soup = BeautifulSoup(html, 'html.parser')
                a = soup.find_all('a',attrs={'target':'_blank'})
                for link in a:
                    path = link.get('href')
                    title = link.get_text()
                    realpath = parse.urljoin(url,path)
                    if len(title.strip()) <= 5 or 'PDF'in realpath or '###'in realpath:
                        pass
                    else:
                        resp1 = requests.get(realpath, headers=headers, timeout=10)
                        resp1.encoding = resp1.apparent_encoding
                        if resp1.status_code == 200:
                            resource = resp1.text
                            bsoup = BeautifulSoup(resource, 'html.parser')
                            nohtml_content = bsoup.find('div',attrs={'class':'page_words'}).get_text().strip().replace('\n','').replace('\r','')
                            content = bsoup.find('div',attrs={'class':'page_words'}).find_all('p')
                            list.append('{}###{}###大连日报###{}###{}'.format(realpath,title,nohtml_content,content))
                    time.sleep(random.randint(0,2))
            else:
                flag = False
    except Exception as e:
        logger.info('=========================大连日报解析异常=========================')
        logger.info(url)
        logger.info(e)
    finally:
        return list


def formatUrl():
    url = getconfig('urls','dlrb')
    date = time.strftime('%Y-%m/%d',time.localtime(time.time()))
    formatUrl = url.format(date,'{}')
    return formatUrl

if __name__ == '__main__':
    list =  parse_url()
    for str in list:
        print(str)
    print(list.__len__())