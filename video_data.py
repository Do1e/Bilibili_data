# coding=gbk
# 获取各项数据 tag存储目标数据类型

def get_data(text, tag):    
    i = text.find(tag)
    while(text[i] > '9' or text[i] < '0'):
        i = i + 1
    for j in range(i, len(text) - 1):
        if(text[j] > '9' or text[j] < '0'):
            break
    return int(text[i:j])
