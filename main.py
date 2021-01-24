# coding=gbk

print('选择功能')
print('1:读取实时粉丝数据')
print('2:读取实时视频数据')
function = input('')
while(function != '1' and function !='2'):
    print('输入错误')
    function = input('')
if(function == '1'):
    from fans import get_num_of_fans
    get_num_of_fans()
elif(function == '2'):
    from video import get_data_of_video
    get_data_of_video()