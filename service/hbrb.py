# -*- coding: utf-8 -*-
import time
import requests
from util.configutil import getconfig
from bs4 import BeautifulSoup
from urllib import parse
from util.LoggerClass import Logger
import random
logger = Logger(logname= 'newspaper',logger='hnrb').getlog()

def parse_url():
    list = []
    tempurl = formatUrl()
    flag = True
    i = 0
    try:
        while flag:
            i += 1
            if i == 1:
                url = tempurl.format('index')
                # print(url)
            else:
                url = tempurl.format('hbrb{}'.format(i))
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
            resp = requests.get(url, headers=headers, timeout=10)
            resp.encoding = resp.apparent_encoding
            html = resp.text
            if resp.status_code == 200:
                soup = BeautifulSoup(html, "html.parser")
                map = soup.find('td',attrs={'class':'style'})
                for link in map.find_all('area',attrs={'shape':'polygon'}):
                    path = link.get('href')
                    title = link.get('alt')
                    realpath = parse.urljoin(url,path)
                    if len(title.strip()) < 4:
                        pass
                    else:
                        resp1 = requests.get(realpath, headers=headers, timeout=10)
                        resp1.encoding = resp1.apparent_encoding
                        if resp1.status_code == 200:
                            resource = resp1.text
                            bsoup = BeautifulSoup(resource, 'html.parser')
                            nohtml_content = bsoup.find('font',attrs={'style':'font-size: 14px;line-height: 26px'}).get_text().strip()
                            content = bsoup.find('font',attrs={'style':'font-size: 14px;line-height: 26px'})
                            list.append('{}###{}###湖北日报###{}###{}'.format(realpath,title,nohtml_content,content))
                        time.sleep(random.randint(0,2))
            else:
                flag = False
    except Exception as ex:
        logger.info('=========================湖北日报解析异常=========================')
        logger.info(url)
        logger.info(ex)
    finally:
        return list


def formatUrl():
    url = getconfig('urls','hbrb')
    date = time.strftime('%Y%m%d',time.localtime(time.time()))
    formatUrl = url.format(date,'{}')
    return formatUrl

if __name__ == '__main__':
    list =  parse_url()
    for str in list:
        print(str)
    print(list.__len__())