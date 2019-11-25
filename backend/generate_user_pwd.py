# coding: utf8
import os, django, sys

sys.path.append('C:\\Users\\biodancer\\Desktop\\typescript\\rstudio_workshop_admin\\backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'backend.settings')
django.setup()


import random,string
from app1 import models
'''
password_count = 100
all_passwds = []
for i in range(int(password_count)):
    num = random.sample(string.digits,1) #随机取1位数字
    lower = random.sample(string.ascii_lowercase,1) #随机取1位小写字母
    upper = random.sample(string.ascii_uppercase,1) #随机取1位大写字母
    other = random.sample(string.ascii_letters+string.digits,5) #随机取5位
    res = num+lower+upper+other #产生的8位密码
    res = ''.join(res)+'\n'
    if res not in all_passwds: #判断是否重复
        all_passwds.append(res)
    else:
        print 'password repeat'

num = 0
for passwd in all_passwds:
    if num < 10:
        num_str = 'test0' + str(num)
    else:    
        num_str = 'test' + str(num)

    userObj = models.linuxUser.objects.create(user = num_str, password = passwd, used = 0)
    userObj.save()
    num +=1
'''
a = models.linuxUser.objects.filter(user='test00')[0]
a.used =0
a.save()     