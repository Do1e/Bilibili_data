# coding=gbk                        #1
import urllib.request               #2
import time                         #3
import openpyxl                     #4
import os                           #5
from name import get_name_of_video  #6
from bv_to_av import get_av         #7
from video_data import get_data     #8

'''
1 转换编码，使代码中允许出现中文
2 用于读取网页信息
3 用于读取时间
4 用于读写Excel文档
5 用于判断文档是否存在
6 获取视频名称
7 将BV号转为av号
8 从网页信息读取视频数据
'''

# 读取视频实时数据并保存至Excel文档中
def get_data_of_video():
    aid = bid = ''
    while(1):
        bid = input('输入视频av号或bv号:')
        if(bid[0:2] != 'av' and bid[0:2] != 'bv' and bid[0:2] != 'BV'):
            print('输入错误')
            continue
        name = get_name_of_video(bid)
        # 读取视频名称
        if(not name):
            print('不存在该视频')
        else:
            if(bid[0:2] != 'av'):
                aid = str(get_av(bid))
            else:
                aid = str(bid[2:])
            # 提取av号
            break
    name = get_name_of_video(bid)
    # 读取视频名称
    stoptime = input('输入采样间隔时间(单位秒):')
    stoptime = int(stoptime)
    # 采样间隔时间，单位是秒
    table_name = name + '.xlsx'
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
        table['B1'] = '播放'
        table['C1'] = '点赞'
        table['D1'] = '投币'
        table['E1'] = '收藏'
        table['F1'] = '弹幕'
        table['G1'] = '分享'
        table['H1'] = '评论'
        table.column_dimensions['A'].width = 21
        Column = ['B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in Column:
            table.column_dimensions[i].width = 8
        # 设置表格列宽
        File.save(table_name)
    # 若此时为空表，则生成表头并设置列宽
    url = 'http://api.bilibili.com/archive_stat/stat?aid=' + aid +'&type=jsonp'
    # 访问该视频数据的api
    prettify = '{:20}\t{:9}\t{:5}\t{:5}\t{:5}\t{:5}\t{:5}\t{:5}'
    print(prettify.format('时间', '播放', '点赞', '投币', '收藏', '弹幕', '分享', '评论'))
    while(1):
        now_time_id = time.time()
        # 读取当前时间戳
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # 按格式读取当前时间
        page = urllib.request.urlopen(url)
        text = page.read()
        # 读取网页内容
        text = text.decode('utf-8')
        view = get_data(text, 'view')
        like = get_data(text, 'like')
        coin = get_data(text, 'coin')
        favorite = get_data(text, 'favorite')
        danmaku = get_data(text, 'danmaku')
        share = get_data(text, 'share')
        reply = get_data(text, 'reply')
        # 读取各项数据
        now_row = [now_time, view, like, coin, favorite, danmaku, share, reply]
        print(prettify.format(str(now_time), str(view), str(like), str(coin), str(favorite), str(danmaku), str(share), str(reply)))
        table.append(now_row)
        # 本次读取插入表格末尾
        File.save(table_name)
        while(1):
            if(time.time() - now_time_id >= stoptime):
                break
        # 保证本段代码运行特定时长
