# -*- coding: UTF-8 -*-
"""
pyinstaller:
https://blog.csdn.net/ming_the_first/article/details/123603971
打包命令：
https://blog.csdn.net/star_platinum2/article/details/123992262?utm_medium=distribute.pc_feed_404.none-task-blog-2~default~BlogCommendFromBaidu~Rate-1-123992262-blog-null.pc_404_mixedpudn&depth_1-utm_source=distribute.pc_feed_404.none-task-blog-2~default~BlogCommendFromBaidu~Rate-1-123992262-blog-null.pc_404_mixedpud
多文件
https://blog.csdn.net/weixin_43347550/article/details/105344993
images:
https://blog.csdn.net/kobeyu652453/article/details/108732747
ico
https://blog.csdn.net/Python_kele/article/details/118495091
https://app.xunjiepdf.com/img2icon/

音乐格式转换在线
https://convertio.co/zh/audio-converter/
音频压缩在线
https://www.compresss.com/cn/compress-audio.html

'''
打包方法：
1，在Explorer中显示，路径行   cmd

2,打包exe
cmd_get_auto()得到命令行，输入
pyinstaller -w -i loli.jpg main.py -p button.py -p event.py -p move.py -p resource -p settings.py -p text_info.py -p 拼图游戏2.py -p 测试1.py --hidden-import button --hidden-import event --hidden-import move --hidden-import resource --hidden-import settings --hidden-import text_info --hidden-import 拼图游戏2 --hidden-import 测试1
-w：不显示控制台，-i:图标

3，打包资源
删除build,dist文件夹.修改spec
datas=[('resource','resource')]

再次打包exe，只打包main.spec
pyinstaller  main.spec
报错去掉-F

4，dist文件夹中找到exe文件

5，减少exe文件包大小的方法
exe文件所在文件夹，按大小排序，从大到小删除文件与文件夹，到exe文件不能运行为止
资源中音乐文件较大
'''
"""
import copy
import os
import sys

import pygame.font


li = pygame.font.get_fonts()
li.sort()
# print(li)

a = pygame.font.match_font('小南同学.ttf')
# print(a)
# print(pygame.font.get_default_font())
# lll = ['microsofthimalaya', 'microsoftjhenghei', 'microsoftjhengheiui', 'microsoftnewtailue', 'microsoftphagspa',
#        'microsoftsansserif', 'microsofttaile', 'microsoftuighur', 'microsoftyahei', 'microsoftyaheiui',
#        'microsoftyibaiti']

# a = random.random()
# print(a)

def run(*args, **kwargs):
    print(args or kwargs)
    a, b = args or kwargs
    print(a)


# run(1, a=3)

def get_images(skillname, *args, filename_prefix=None, **kwargs):
    if filename_prefix is None:
        filename_prefix = './素材/外星人/'
    
    character_filename = filename_prefix + skillname
    
    image = pygame.image.load(character_filename)
    # image = Image.open('./素材/人物/' + moe_sister + '.png')
    wid, hid = image.get_size()
    
    rows, columns = None, None
    if not args:
        rows, columns = kwargs.get('rows'), kwargs.get('columns')
        print(rows, columns, kwargs)
    if not kwargs:
        rows, columns = args
    
    pos = wid, hid, rows, columns
    print(pos)
    # images = self.load_image(character_filename, *pos)


# get_images('alien.jpg', 2, 2)
# get_images('alien.jpg', rows=2, columns=2)

# pyinstaller  lcc.py -p util.py -p setting.py -p Button.py -p Study.py -p StudySecond.py -p StudyThird.py -p
# Advanced.py --hidden-import util --hidden-import setting  --hidden-import Button --hidden-import Study
# --hidden-import StudySecond --hidden-import StudyThird --hidden-import Advenced

# pyinstaller -F -w main.py


# # coding:utf-8
# import sys
# import os

# 生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 访问res文件夹下数据.txt的内容
filename = resource_path(os.path.join("素材", "外星人", '亚丝娜.png'))
print(filename)
#
# # with open(filename, encoding='utf-8') as f:
# #     lines = f.readlines()
# #     print(lines)
# #     f.close()

def get_cmd(ico, main, *args):
    '''
    获取打包文件的命令
    :param main:
    :param args:
    :return:
    '''
    a = 'pyinstaller ' + '-w ' + '-i ' + ico + ' ' + main + ' '
    
    b = ''
    c = ''
    for item in args:
        be = '-p' + ' ' + item + ' '
        b += be
        # print('a.py'.split('.')[0])
        ce = '--hidden-import' + ' ' + item.split('.')[0] + ' '
        c += ce
    
    d = a + b + c
    return d


# e = get_cmd('loli.ico', 'main.py', 'alien.py', 'animation_realize.py', 'bullet.py', 'button_1.py', 'event.py',
#             'game_stats.py', 'player_active.py', 'scoreboard.py', 'settings.py', 'ship.py')
# print(e)

# abstruct_path = './素材/音乐'
# print(os.listdir(abstruct_path))

'''
python安装教程
https://blog.csdn.net/weixin_49237144/article/details/122915089
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager


def example():
    # 票房单位亿元
    movies = {
        "流浪地球": 40.78,
        "飞驰人生": 15.77,
        "疯狂的外星人": 20.83,
        "新喜剧之王": 6.10,
        "廉政风云": 1.10,
        "神探蒲松龄": 1.49,
        "小猪佩奇过大年": 1.22,
        "熊出没·原始时代": 6.71
    }
    # 中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 13
    # 设置图大小
    plt.figure(figsize=(15, 8))
    
    x = list(movies.keys())  # 获取x轴数据(字典的键)
    y = list(movies.values())  # 获取y轴数据(字典的值)
    
    plt.bar(x, y, width=0.5, bottom=0, align='edge', color='g', edgecolor='r', linewidth=2)
    
    # 绘制标题
    plt.title("电影票房数据", size=26)
    
    # 设置轴标签
    plt.xlabel("电影名", size=28)
    plt.ylabel("票房/亿", size=28)
    
    plt.show()
    
    # print('werfc' + 'fgvergs')


path_list = os.listdir('../消灭外星人重置版')
ico, main = 'loli.ico', 'main.py'
# path_list = copy.deepcopy(path_list)
path_list.remove(ico)
path_list.remove(main)
path_list.remove('素材')
# print(path_list)

cmd = get_cmd(ico, main, *path_list)
# print(cmd)
