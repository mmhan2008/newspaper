# -*- coding: utf-8 -*-
import time
import requests
from util.configutil import getconfig
from bs4 import BeautifulSoup
from urllib import parse
from util.LoggerClass import Logger
import random
logger = Logger(logname= 'newspaper',logger='gzrb').getlog()

def parse_url():
    list = []
    tempurl = formatUrl()
    # print(tempurl)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        resp = requests.get(tempurl, headers=headers, timeout=10)
        resp.encoding = resp.apparent_encoding
        html = resp.text
        if resp.status_code == 200:
            soup = BeautifulSoup(html, 'html.parser')
            a = soup.find_all('a')
            for link in a:
                path = link.get('href')
                title = link.get_text().strip().replace('\n','').replace('\r','')
                realpath = parse.urljoin(tempurl,path)
                keys = ['首页','广告','报','版','往期','舞台与银幕','大洋网','网站地图','公众号','黄页']
                if any(key in title for key in keys) or title == '':
                    pass
                else:
                    resp1 = requests.get(realpath, headers=headers, timeout=10)
                    resp1.encoding = resp1.apparent_encoding
                    if resp1.status_code == 200:
                        resource = resp1.text
                        bsoup = BeautifulSoup(resource, 'html.parser')
                        nohtml_content = bsoup.find('founder-content').get_text().strip()
                        content = bsoup.find('founder-content').find_all('p')
                        list.append('{}###{}###广州日报###{}###{}'.format(realpath,title,nohtml_content,content))
                    time.sleep(random.randint(0,2))
    except Exception as e:
        logger.info('=========================广州日报解析异常=========================')
        logger.info(tempurl)
        logger.info(e)
    finally:
        return list


def formatUrl():
    url = getconfig('urls','gzrb')
    date1 = time.strftime('%Y-%m/%d',time.localtime(time.time()))
    date2 = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    formatUrl = url.format(date1,date2)
    return formatUrl

if __name__ == '__main__':
    list =  parse_url()
    for str in list:
        print(str)
    print(list.__len__())