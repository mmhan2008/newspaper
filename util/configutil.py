# -*- coding: utf-8 -*-
import os
import configparser

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# config.ini文件路径
config_path = os.path.join(root_path, 'config/resource.ini')
config = configparser.RawConfigParser()
config.read(config_path,encoding='utf-8')

def getconfig(section,option):
    return config.get(section,option)

def getoptions(opt):
    return config.options(opt)
