# -*- coding: utf-8 -*-
import time
import random
import requests
from util.configutil import getconfig
from bs4 import BeautifulSoup
from urllib import parse
from util.LoggerClass import Logger

logger = Logger(logname= 'newspaper',logger='jfrbsh').getlog()

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
            if html != '':
                soup = BeautifulSoup(html, 'html.parser')
                div = soup.find_all('div',attrs={'class':'list'})
                for a in div:
                    for link in a.find_all('a'):
                        path = link.get('href')
                        title = link.get_text().strip()
                        realpath = parse.urljoin(url,path)
                        if len(title.strip()) <= 4:
                            pass
                        else:
                            resp1 = requests.get(realpath, headers=headers, timeout=10)
                            resp1.encoding = resp1.apparent_encoding
                            if resp1.status_code == 200:
                                resource = resp1.text
                                bsoup = BeautifulSoup(resource, 'html.parser')
                                nohtml_content = bsoup.find('div', attrs={'class': 'content'}).get_text().strip()
                                content = bsoup.find('div', attrs={'class': 'content'})
                                list.append('{}###{}###解放日报(上海)###{}###{}'.format(realpath,title,nohtml_content,content))
                            time.sleep(random.randint(0, 2))
            else:
                flag = False
    except Exception as e:
        logger.info('=========================解放日报(上海)解析异常=========================')
        logger.info(url)
        logger.info(e)
    finally:
        return list


def formatUrl():
    url = getconfig('urls','jfrbsh')
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    formatUrl = url.format(date,'{}')
    return formatUrl

if __name__ == '__main__':
    list =  parse_url()
    for str in list:
        print(str)
    print(list.__len__())