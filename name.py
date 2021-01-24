# coding=gbk
from bs4 import BeautifulSoup
import urllib.request
import gzip
from io import BytesIO

# 读取该up主的昵称
def get_name_of_up(UID):
    url = 'https://api.bilibili.com/x/space/acc/info?mid=' + UID + '&jsonp=jsonp'
    page = urllib.request.urlopen(url)
    text = page.read()
    text = text.decode('utf-8')
    # 昵称中可能存在中文，需要进行编码转换
    i = text.find('name')
    i = i + 7
    for j in range(i, len(text)-1):
        if(text[j] == '"'):
            break
    if(not text[i:j]):
        return None
    return text[i:j]

# 读取视频名称
def get_name_of_video(av_or_bv):
    url = 'https://www.bilibili.com/video/' + av_or_bv
    Header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51'}
    page = urllib.request.Request(url=url, headers=Header)
    contents = urllib.request.urlopen(page)
    contents = BytesIO(contents.read())
    contents = gzip.GzipFile(fileobj=contents)
    contents = contents.read().decode('utf-8')
    # 读取与编码
    soup = BeautifulSoup(contents, 'html.parser')
    title = soup.find('h1', class_='video-title')
    # 用BeautifulSoup查找名字
    if(not title):
        return None
    return title.text
