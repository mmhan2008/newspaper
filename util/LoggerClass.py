# -*- coding: UTF-8 -*-
import logging
import datetime
import os

class Logger():
    def __init__(self, logname,logger):
        '''
         指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
         '''

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        file_name = '%s/logs/%s%s.log'%(root_path,logname,datetime.datetime.now().strftime("%Y-%m-%d"))
        fh = logging.FileHandler(file_name,encoding='utf-8')
        fh.setLevel(logging.INFO)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s-%(filename)s %(lineno)d %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


    def getlog(self):
        return self.logger
