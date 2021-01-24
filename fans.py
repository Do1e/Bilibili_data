# coding=gbk                        #1
import urllib.request               #2
import time                         #3
import openpyxl                     #4
import os                           #5
from name import get_name_of_up     #6

'''
1 转换编码，使代码中允许出现中文
2 用于读取网页信息
3 用于读取时间
4 用于读写Excel文档
5 用于判断文档是否存在
6 获取昵称
'''

# 读取up主实时粉丝数并保存至Excel文档中
def get_num_of_fans():
    while(1):
        uid = input('输入B站uid:')
        name = get_name_of_up(uid)
        if(not name):
            print('不存在该用户')
        else:
            break
    # 读取该up主的昵称
    stoptime = input('输入采样间隔时间(单位秒):')
    stoptime = int(stoptime)
    # 采样间隔时间，单位是秒
    table_name = name + '的实时粉丝数.xlsx'
    # 保存的Excel文件名
    if(not os.path.exists(table_name)):
        File = openpyxl.Workbook()
        try:
            File.save(table_name)
        except OSError:
            print('包含特殊字符，无法按原名称保存')
            table_name = table_name.replace('\\', ' ')
            table_name = table_name.replace('/', ' ')
            table_name = table_name.replace(':', ' ')
            table_name = table_name.replace('*', ' ')
            table_name = table_name.replace('?', ' ')
            table_name = table_name.replace('"', ' ')
            table_name = table_name.replace('<', ' ')
            table_name = table_name.replace('>', ' ')
            table_name = table_name.replace('|', ' ')
            File.save(table_name)
    # 若不存在文件，则新建文件
    File = openpyxl.load_workbook(table_name)
    table = File[File.sheetnames[0]]
    # 读取文档的第一个表格
    if(not table['A1'].value):
        table['A1'] = '时间'
        table['B1'] = '粉丝数'
        table.column_dimensions['A'].width = 21
        table.column_dimensions['B'].width = 8
        # 设置表格列宽
        File.save(table_name)
    # 若此时为空表，则生成表头并设置列宽
    url = 'https://api.bilibili.com/x/relation/stat?vmid=' + uid +'&jsonp=jsonp'
    # B站读取粉丝数的api
    while(1):
        now_time_id = time.time()
        # 读取当前时间戳
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # 按格式读取当前时间
        page = urllib.request.urlopen(url)
        text = page.read()
        # 读取网页内容
        text = text.decode('utf-8')
        i = text.find('follower')
        i = i + 10
        for j in range(i, len(text) - 1):
            if(text[j] > '9' or text[j] < '0'):
                break
        # 取得粉丝数
        print(now_time)
        print('当前粉丝数:' + text[i: j])
        now_row = [now_time, int(text[i: j])]
        table.append(now_row)
        # 本次读取插入表格末尾
        File.save(table_name)
        while(1):
            if(time.time() - now_time_id >= stoptime):
                break
        # 保证本段代码运行特定时长

get_num_of_fans()