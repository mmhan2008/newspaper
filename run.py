# -*- coding: utf-8 -*-
import importlib
import queue
import threading
import time

from service import *
from datetime import datetime,date
from util import configutil
from util import esutil
from util.LoggerClass import Logger

logger = Logger(logname= 'newspaper',logger='run').getlog()
#任务列表
options = []
q = queue.Queue()

def fetchUrl(q):
    while True:
        try:
            taskName = q.get_nowait()
            name = importlib.import_module('.%s'%taskName,package='service')
        except Exception as e:
            logger.info(e)
            break
        # print('Current Thread Name %s, Url: %s ' % (threading.currentThread().name,taskName))
        try:
            result = name.parse_url()
            for kv in  result:
                es_operate(kv)
            if result.__len__() != 0:
                options.remove(taskName)
            logger.info('%s日报共获取%s条新闻'%(taskName,result.__len__()))
        except Exception as e:
            logger.info(e)
            continue
        time.sleep(1)

def es_operate(href):
    try:
        temp = href.split('###')
        link = temp[0]
        urlmd5 = esutil.format_md5(link)
        if esutil.query_data('gather_paper','document',urlmd5):
            pass
        else:
            data = {
                'source': temp[2],
                'c_time': datetime.now().replace(microsecond=0),
                'p_date': date.today(),
                'url': link,
                'title': temp[1],
                'code': urlmd5,
                'nohtml_content': temp[3],
                'content': temp[4],
            }
            esutil.insert_single_data('gather_paper','document',data,urlmd5)
    except Exception as e:
        logger.info(e)

def open_thread():
    startTime = time.time()
    threads = []
    threadNum = 10
    for i in range(0,threadNum):
        t = threading.Thread(target=fetchUrl,args=(q,))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    endTime = time.time()
    logger.info('任务结束，总计耗时: %s秒' %  (endTime - startTime))


def test():
    print('当前时间:%s'%datetime.datetime.now().strftime("%Y-%m-%d %X"))
    print('8888888888888888888888')

#任务入口
def entrance():
    #初始化任务队列
    global options,q
    options = configutil.getoptions('urls')
    flag = True
    endTime = '10:00:00'
    i = 0
    while flag:
        i += 1
        for opt in options:
            q.put(opt)
        logger.info('-----------------第%s次爬取开始，当前队列中还有%s个网站需要处理-----------------'%(i,q.qsize()))
        open_thread()
        nowTime = datetime.now().strftime('%X')
        if endTime < nowTime or options.__len__() == 0:
            flag = False
            logger.info('================================今日任务已完成,爬虫进入休眠状态================================')
        else:
            time.sleep(1800)

if __name__ == '__main__':
    logger.info('================================日报爬虫开始工作================================')
    entrance()
