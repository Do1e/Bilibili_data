# coding=gbk

print('ѡ����')
print('1:��ȡʵʱ��˿����')
print('2:��ȡʵʱ��Ƶ����')
function = input('')
while(function != '1' and function !='2'):
    print('�������')
    function = input('')
if(function == '1'):
    from fans import get_num_of_fans
    get_num_of_fans()
elif(function == '2'):
    from video import get_data_of_video
    get_data_of_video()