# -*- coding: utf-8 -*-

import hashlib
import time

from elasticsearch import Elasticsearch

from util import configutil
from util.LoggerClass import Logger

logger = Logger(logname= 'newspaper',logger='esutil').getlog()
try:
    host = configutil.getconfig('eshost', 'host')
    port = configutil.getconfig('eshost', 'port')
    es = Elasticsearch([{'host':host,'port':port}])
except Exception as ex:
    logger.info(ex)

def insert_single_data(index_name,doc_type,data,esid):
    try:
        res = es.index(index=index_name, doc_type=doc_type, body=data,id=esid)
        return res
    except Exception as e:
        logger.info(e)


def insert_datas(index_name,doc_type,datas):
    try:
        res = es.bulk(index=index_name, doc_type=doc_type,body=datas)
        return res
    except Exception as e:
        logger.info(e)

def query_data(index_name,doc_type,urlmd5):
    return es.exists(index=index_name, doc_type=doc_type,id = urlmd5)

def format_md5(st):
    return hashlib.md5(st.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    da = 'http://www.forestry.gov.cn/main/72/20190320/093452504668812.html'
    urlmd5 = hashlib.md5(da.encode('utf-8')).hexdigest()
    print(urlmd5)
    data = {'c_time':int(round(time.time() * 1000)),
            'url':da,
            'title':'近自然育林　提森林质量',
            'code':urlmd5}
    # insert_single_data('newspaper_index','newspaper_type',data,urlmd5)
    res = query_data('newspaper_index','newspaper_type',urlmd5)
    print(res)