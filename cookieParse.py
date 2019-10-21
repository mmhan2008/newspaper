# -*- coding: UTF-8 -*-
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from util import configutil
from util import esutil
from urllib import parse
from util.LoggerClass import Logger

logger = Logger(logname= 'cookieParse',logger='cookieParse').getlog()
sched = BlockingScheduler()

def cookie_Parse(url):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('blink-settings=imagesEnabled=false')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        time.sleep(5)
        return driver.page_source
    except Exception as e:
        logger.info('{}在使用cookie_Parse方法解析时，过程出现异常\n{}'.format(url,e))
        return '解析过程出现异常'
    finally:
        driver.quit()

def cookieurl_1():
    url = configutil.getconfig('cookieurl','1')
    page = cookie_Parse(url)
    soup = BeautifulSoup(page, 'html.parser')
    name = soup.title.text
    try:
        tbody = soup.find('tbody', attrs={'id': 'contentBody'})
        for link in tbody.find_all('a'):
            href = link.get('href')
            title = link.get_text()
            urlMd5 = esutil.format_md5(href)
            if esutil.query_data('spidernews_index', 'spidernews_type', urlMd5):
                pass
            else:
                data = {
                    'link':href,
                    'name': name,
                    'createTime': int(round(time.time() * 1000)),
                    'title': title,
                    'urlMd5': urlMd5,
                }
                esutil.insert_single_data('spidernews_index', 'spidernews_type', data, urlMd5)
    except Exception as e :
        logger.info(e)

def cookieurl_2():
    url = configutil.getconfig('cookieurl', '2')
    page = cookie_Parse(url)
    soup = BeautifulSoup(page, 'html.parser')
    name = soup.title.text
    try:
        tbody = soup.find('div', attrs={'class': 'main'})
        for link in tbody.find_all('a'):
            href = link.get('href')
            real_path = parse.urljoin(url,href)
            title = link.get_text()
            urlMd5 = esutil.format_md5(real_path)
            if esutil.query_data('spidernews_index', 'spidernews_type', urlMd5):
                pass
            else:
                data = {
                    'link': real_path,
                    'name': name,
                    'createTime': int(round(time.time() * 1000)),
                    'title': title,
                    'urlMd5': urlMd5,
                }
                esutil.insert_single_data('spidernews_index', 'spidernews_type', data, urlMd5)
    except Exception as e:
        logger.info(e)

def cookieurl_3():
    url = configutil.getconfig('cookieurl', '3')
    page = cookie_Parse(url)
    soup = BeautifulSoup(page, 'html.parser')
    name = soup.title.text
    try:
        tbody = soup.find('td', attrs={'class': '2016_erji_content'})
        for link in tbody.find_all('a'):
            href = link.get('href')
            real_path = parse.urljoin(url,href)
            title = link.get_text()
            urlMd5 = esutil.format_md5(real_path)
            if esutil.query_data('spidernews_index', 'spidernews_type', urlMd5):
                pass
            else:
                data = {
                    'link': real_path,
                    'name': name,
                    'createTime': int(round(time.time() * 1000)),
                    'title': title,
                    'urlMd5': urlMd5,
                }
                print(data)
                esutil.insert_single_data('spidernews_index', 'spidernews_type', data, urlMd5)
    except Exception as e:
        logger.info(e)

if __name__ == '__main__':
    cookieurl_1()
    cookieurl_2()
    cookieurl_3()