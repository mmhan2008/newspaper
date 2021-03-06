# -*- coding: utf-8 -*-
import time
import requests
from util.configutil import getconfig
from bs4 import BeautifulSoup
from urllib import parse
from util.LoggerClass import Logger
import random
logger = Logger(logname= 'newspaper',logger='fjrb').getlog()

def parse_url():
    list = []
    tempurl = formatUrl()
    flag = True
    i = 21
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
                # print(soup.prettify())
                tbody = soup.find_all('tbody')[1]
                for link in tbody.find_all('a'):
                    path = link.get('href')
                    title = link.get_text()
                    realpath = parse.urljoin(url,path)
                    resp1 = requests.get(realpath, headers=headers, timeout=10)
                    resp1.encoding = resp1.apparent_encoding
                    if resp1.status_code == 200:
                        resource = resp1.text
                        bsoup = BeautifulSoup(resource, 'html.parser')
                        nohtml_content = bsoup.find('td', attrs={'class': 'xilan_content_tt'}).get_text().strip()
                        content = bsoup.find('td', attrs={'class': 'xilan_content_tt'}).find_all('p')
                        list.append('{}###{}###福建日报###{}###{}'.format(realpath,title,nohtml_content,content))
                    time.sleep(random.randint(0,2))
            else:
                flag = False
    except Exception as e:
        logger.info('=========================福建日报解析异常=========================')
        logger.info(url)
        logger.info(e)
    finally:
        return list


def formatUrl():
    url = getconfig('urls','fjrb')
    date = time.strftime('%Y-%m/%d',time.localtime(time.time()))
    formatUrl = url.format(date,'{}')
    return formatUrl

if __name__ == '__main__':
    # html = """ <html><head><title>The Dormouse's story</title></head> <body> <p class="title" name="dromouse"><b>The Dormouse's story</b></p> <p class="story">Once upon a time there were three little sisters; and their names were <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>, <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>; and they lived at the bottom of a well.</p> <p class="story">...</p> """
    # soup = BeautifulSoup(html, 'html.parser')
    # for link in soup.find_all('a'):
    #     print(link.get_text())
    list =  parse_url()
    for str in list:
        print(str)
    print(list.__len__())