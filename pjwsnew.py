# coding=utf-8
import base64
import datetime
import json
import time
import random
import uuid
from pprint import pprint

import execjs
import requests
from Cryptodome.Cipher import DES3
from Cryptodome.Util.Padding import unpad
from selenium import webdriver

from util import esutil
from util.LoggerClass import Logger
from util.configutil import getconfig

"""
2019年9月份文书网spider更新，简单看了下文书网更新过后的加密方式，整体比以前简单不少，
总结起来大概就是ciphertext这个参数是变化的，其他的基本上不会改变，传入data获取数据后，会有一个
DES3解密，其他的好像没什么难点（有可能没遇到坑），就大概写个逻辑脚本，需要完善
"""
logger = Logger(logname='pjws', logger='pjws').getlog()

# ----------------------------------自定义函数-------------------------------------------


def get_cookie():
    driver = webdriver.Chrome()
    driver.get('http://wenshu.court.gov.cn')
    cookie = driver.get_cookie('SESSION').get('value')
    print(cookie)
    return cookie

# 获取ciphertext参数


def get_cipher():
    with open(r'strTobinary.js', encoding='utf-8') as fp:
        js = fp.read()
        ect = execjs.compile(js)
        cipherText = ect.call('cipher')
        return cipherText

# 获取DES解密后的返回值


def get_result(result, secretKey, date):
    des3 = DES3.new(key=secretKey.encode(),
                    mode=DES3.MODE_CBC, iv=date.encode())
    decrypted_data = des3.decrypt(base64.b64decode(result))
    plain_text = unpad(decrypted_data, DES3.block_size).decode()
    return plain_text

# 获取__RequestVerificationToken参数


def get_token():
    js = """ function random(size){
            	var str = "",
            	arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
            	for(var i=0; i<size; i++){
            		str += arr[Math.round(Math.random() * (arr.length-1))];
            	}
            	return str;
            }
    """
    ctx = execjs.compile(js)
    result = ctx.call("random", "24")
    return result

# 获取pageid


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


def get_session():
    uids = str(uuid.uuid4()).split('-')
    return uids[0]+'-' + uids[1] + '-' + uids[2] + '-' + uids[3] + '-' + uids[4]


def confirm(string):
    try:
        url = getconfig('companycheck', 'address')+string
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

# -------------------------------自定义函数结束-----------------------------------------


class wenshu(object):
    def __init__(self):
        self.session = requests.Session()
        self.proxies = [
            {"http": "47.111.24.165:5000"},
            {"http": "47.94.209.31:5000"},
            {"http": "47.105.62.16:5000"}
        ]
    def get_docid(self,keyword):
        """文书列表页"""
        url = "http://wenshu.court.gov.cn/website/parse/rest.q4w"
        # today = datetime.datetime.now().strftime('%Y-%m-%d ')
        yesterday = datetime.date.today() + datetime.timedelta(-1)
        pageId = get_pageid()
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "_gscu_2116842793=67060699jbu1vk18; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1567060699; HM4hUBT0dDOn80S=9weMDXwjC3bkKJ4DSjXLWFyBQc2R8lS9giUGIRA6S1NwymF2pR9Xy6tfwx2eG2Je; HM4hUBT0dDOn80T=4GxHy2acsJZtRwJIX26h0Of1C85_OzVm56GC0eiaFiLKIBEaQtTiFgFbJS8gDMQI0N3ZuitgayVpsuLOgMRgu.DRjJENT0QIlswOGj_PESU0Utpv3rfJKcVWGx76DFD3o1islNr6RE0HA6kw4ixIsElfL3ASV6HTZVr3WSHQf8nwS22h4v2oPA5u96dASw1yxbYF3rtIBV7CFZQ7COxNteE_b3WwNG6zXs4BxauNolLZmKaAD2EPHpViRkc8UqXIy_YC6JT1.zKmBKaGILUn4VPRDOc_PjbHRx0DDJcxOAVsHr.52n6ijUZCt0IbpdHNSAz3;SESSION=%s" % get_session(),
            "Host": "wenshu.court.gov.cn",
            "Origin": "http://wenshu.court.gov.cn",
            "Proxy-Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            # "Referer": "http://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=%s&s21=%s&cprqStart=%s" % (pageId,keyword,yesterday),
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"
        }
        try:
            data = {
                "pageId": "%s" % pageId,
                "s21": "%s" % keyword,
                "cprqStart": "%s" % yesterday,
                "sortFields": "s51:desc",  # 按照日期降序排列
                "ciphertext": "%s" % get_cipher(),
                "pageNum": "1",
                "pageSize": "15",
                "queryCondition": '[{"key":"s21","value":"%s"},{"key":"cprq","value":"%s TO 2099-01-01"}]' % (keyword,yesterday),
                "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc",
                "__RequestVerificationToken": "%s" % get_token()
            }
            response = self.session.post(
                url, data=data, headers=headers,proxies=self.proxies[random.randint(0, 2)]).text
            json_value = json.loads(response)
            secretKey = json_value["secretKey"]
            result = json_value["result"]
            data = json.loads(get_result(result, secretKey, time.strftime("%Y%m%d")))
            # pprint(data["queryResult"]["resultList"])
            # 获取详细信息，数据判别保存
            i = 0
            j = 0
            for key in data["queryResult"]["resultList"]:
                i += 1
                if esutil.query_data('spidernews_index', 'spidernews_type', key['rowkey']):
                    pass
                else:
                    j += 1
                    data = {
                        'link': 'http://wenshu.court.gov.cn/website/wenshu/181107ANFZ0BXSK4/index.html?docId=%s' % key['rowkey'],
                        'name': '中国裁判文书网 ' + keyword,
                        'createTime': int(round(time.time() * 1000)),
                        'title': key['1'] + '，裁判日期：' + key['31'],
                        'casenumber': key['7'],
                        'court': key['2'],
                        'urlMd5': key['rowkey'],
                    }
                    esutil.insert_single_data(
                        'spidernews_index', 'spidernews_type', data, key['rowkey'])
            logger.info('本次抓取总计获取数据%s,存入es的数据%s' % (i, j))
            # rowkey = key["rowkey"]
            # self.detail_page(rowkey)
        except Exception as e:
            logger.info(e)

    def detail_page(self, docid):
        """文书详情页"""
        url = "http://wenshu.court.gov.cn/website/parse/rest.q4w"
        data = {
            "docId": "%s" % docid,
            "ciphertext": get_cipher(),
            "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch",
            "__RequestVerificationToken": "%s" % get_token(),
        }

        response = self.session.post(url, data=data, headers=self.headers)
        json_value = json.loads(response.text)
        secretKey = json_value["secretKey"]
        result = json_value["result"]
        data = json.loads(get_result(
            result, secretKey, time.strftime("%Y%m%d")))
        print(data)


if __name__ == '__main__':
    demo = wenshu()
    logger.info('==================开始抓取证券部分==================')
    demo.get_docid('%E9%93%B6%E8%A1%8C')
    time.sleep(random.randint(30, 120))
    logger.info('++++++++++++++++++开始抓取银行部分++++++++++++++++++')
    demo.get_docid('银行')
    time.sleep(random.randint(30, 120))
    logger.info('~~~~~~~~~~~~~~~~~~开始抓取信托部分~~~~~~~~~~~~~~~~~~')
    demo.get_docid('信托')