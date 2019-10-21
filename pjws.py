# -*- coding: UTF-8 -*-

import datetime
import json
import random
import time
from urllib import parse

import execjs
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from util import esutil
from util.LoggerClass import Logger
from util.configutil import getconfig

logger = Logger(logname= 'pjws',logger='pjws').getlog()

user_agents = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    ]
proxy = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": 'http-pro.abuyun.com',
    "port": 9010,
    "user": 'H033BRX5880I852P',
    "pass": 'C60284018BE3A6ED',
}
def grab(url,server):
    results = []
    options = Options()
    options.add_argument('user-agent=%s'%user_agents[random.randint(0, 34)])
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--proxy-server=%s'%server)
    options.add_argument('blink-settings=imagesEnabled=false')
    # options.add_argument('window-size=1980,1080')  #无头模式坑
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(30)
    try:
        driver.get(url)
        time.sleep(random.randint(1,3))
        gjjs = driver.find_element_by_xpath('//*[@class="advenced-search"]')
        gjjs.click()
        firstday = datetime.date.today().replace(day=1).strftime('%Y-%m-%d')
        today = datetime.datetime.now().strftime('%Y-%m-%d ')
        driver.find_element_by_id('cprqStart').send_keys(firstday)
        # driver.find_element_by_xpath('//*[@id="cprqEnd"]').send_keys(today)
        searchbt = driver.find_element_by_xpath('//*[@id="searchBtn"]')
        searchbt.click()
        # 下一页按钮
        nextPageBtn = driver.find_element_by_link_text(u'下一页')
        time.sleep(random.randint(1, 10))
        sortbt = driver.find_element_by_xpath('//*[@id="_view_1545184311000"]/div[2]/div[2]/a')
        sortbt.click()
        time.sleep(random.randint(1,10))
        pagebt = driver.find_element_by_xpath('//*[@class="pageSizeSelect"]')
        pagebt.click()
        time.sleep(random.randint(1,10))
        option = driver.find_element_by_xpath('//*[@class="pageSizeSelect"]/option[3]')
        option.click()
        time.sleep(random.randint(1,10))
        lists = driver.find_elements_by_class_name('LM_list')
        if lists:
            i = 0
            while True:
                if i * 15 > 60:
                    i = 0
                    break
                i += 1
                source = driver.find_elements_by_class_name('LM_list')
                if source:
                    pagesource = driver.page_source
                    soup = BeautifulSoup(pagesource, 'html.parser')
                    divs = soup.find_all('div', attrs={'class': 'LM_list'})
                    for elem in divs:
                        a = elem.find('a', attrs={'class': 'caseName'})
                        riqi = elem.find('span', attrs={'class', 'cprq'})
                        casename = a.get_text().strip()
                        path = a.get('href')
                        realpath = parse.urljoin(url, path)
                        date = riqi.get_text()
                        results.append('%s###%s###%s' % (casename, realpath, date))
                else:
                    continue
                nextPageBtn.click()
                time.sleep(random.randint(1, 10))
    except Exception as e:
        logger.info('未获取到数据')
        logger.info(e)
    finally:
        driver.quit()
        return results

def confirm(string):
    try:
        url = getconfig('companycheck','address')+string
        resp = requests.get(url)
        # print(resp.text)
        result = json.loads(resp.text)
        if result.get('code') == '2':
            return True
        else:
            return False
    except Exception as e:
        logger.info(e)
        return False

def es_operate(list):
    i = 0
    j = 0
    if list:
        try:
            for title in list:
                spl = title.split('###')
                if confirm(spl[0]):
                    i += 1
                    urlmd5 = esutil.format_md5(spl[1])
                    if esutil.query_data('spidernews_index', 'spidernews_type', urlmd5):
                        pass
                    else:
                        # text = get_text(spl[1])
                        data = {
                            'link':spl[1],
                            'name': '判决文书网',
                            'createTime':int(round(time.time() * 1000)),
                            'title': spl[0]+'，发布日期：'+spl[2],
                            'urlMd5': urlmd5,
                            # 'content':text
                        }
                        esutil.insert_single_data('spidernews_index','spidernews_type',data,urlmd5)
                        j += 1
            logger.info('本次总计抓取数据%s条，符合条件的数据总计%s条，存入es的数据有%s条'%(len(list),i,j))
        except Exception as e:
            logger.info(e)

def get_text(url):
    result=''
    options = Options()
    # options.add_argument('user-agent=%s' % user_agents[random.randint(0, 34)])
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--proxy-server=%s'%proxy)
    options.add_argument('blink-settings=imagesEnabled=false')
    # options.add_argument('window-size=1980,1080')
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(120)
    try:
        driver.get(url)
        time.sleep(random.randint(1,3))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.find('div', attrs={'class': 'PDF_pox'})
        if text:
            result =  text.get_text().strip()
    except Exception as e:
        logger.info(e)
    finally:
        driver.quit()
        return result
def get_pageid():
    js = """function happy() {
                    var guid = "";
                    for (var i = 1; i <= 32; i++) {
                        var n = Math.floor(Math.random() * 16.0).toString(16);
                        guid += n;
                        // if ((i == 8) || (i == 12) || (i == 16) || (i == 20)) guid +=
                        // "-";
                    }
                    return guid;
                }"""
    ctx = execjs.compile(js)
    pageid = ctx.call("happy")
    return pageid

if __name__ == '__main__':
    servers=['47.111.24.165:5000','47.94.209.31:5000','47.105.61.16:5000']
    ser = random.choice(servers)
    logger.info('本次工作ip : %s'%ser)
    logger.info('=========================开始抓取政府网站案件=========================')
    logger.info('~~~~~~~~~~~~~~~~~~~证券部分~~~~~~~~~~~~~~~')
    zq = getconfig('pjws','address1').format(get_pageid())
    result = grab(zq,ser)
    for i in result:
        logger.info('%s、%s' % (result.index(i) + 1, i))
    es_operate(result)
    time.sleep(random.randint(100,300))
    logger.info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    logger.info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    logger.info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    logger.info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    ser = random.choice(servers)
    logger.info('本次工作ip : %s' % ser)
    logger.info('~~~~~~~~~~~~~~~~~~~银行部分~~~~~~~~~~~~~~~')
    yh = getconfig('pjws','address2').format(get_pageid())
    result1 = grab(yh,ser)
    for i in result1:
        logger.info('%s、%s' % (result1.index(i) + 1, i))
    es_operate(result1)

