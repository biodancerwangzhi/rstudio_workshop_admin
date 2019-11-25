#-*- coding: utf-8 -*-
import os, django, sys
reload(sys)
sys.setdefaultencoding('utf8')

# develop
'''
sys.path.append('C:\\Users\\biodancer\\Desktop\\typescript\\rstudio_workshop_admin\\backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'backend.settings')
django.setup()
'''
from django.conf import settings

from django.shortcuts import render, HttpResponse, redirect
# develop
import models
#from app1 import models 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
#from django.core.mail import send_mail
import smtplib
from email.mime.text import MIMEText
from email.header import Header

try:
    smtp = smtplib.SMTP_SSL()
    smtp.connect(settings.EMAIL_HOST, settings.EMAIL_PORT)
    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)  
except Exception,e:
    print "smtp.connect:",str(e)
    exit()

EMAIL_TEMPLETE = ''' 
您好，{{ username }}
您的rstudio server用户名：{{ linuxUser }}
密码：{{ linuxPwd }}
访问地址是http：//192.168.1.8:8787
欢迎您使用上述平台完成此次workshop学习，
感谢您的参与。  
'''

def generate_email_content(username, linuxUser, linuxPwd):
    new_email = EMAIL_TEMPLETE
    new_email = new_email.replace('{{ username }}', username)
    new_email = new_email.replace('{{ linuxUser }}', linuxUser)
    new_email = new_email.replace('{{ linuxPwd }}', linuxPwd)
    message = MIMEText(new_email, 'plain', 'utf-8')
    message['From'] = Header('Rstudio workshop', 'utf-8')
    message['to'] = Header('用户', 'utf-8')
    return message

def send_email(email, email_content):
    email_title = "rstudio workshop username and password"
    email_content['Subject'] = Header(email_title, 'utf-8')
    try:
        smtp.sendmail(settings.EMAIL_HOST_USER, [email], email_content.as_string())
        send_status = 1
    except:
        send_status = 0
    return send_status

def get_linux_user_pwd():
    try:
        userObjs = models.linuxUser.objects.filter(used=0)
        userObj = userObjs[0]
        userObj.used = 1
        userObj.save()
        return 1, userObj.user, userObj.password
    except:
        return 0, '', ''

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        studentId = request.POST.get('studentId')
        email = request.POST.get('email')

        ret = {'status': 0, 'Info': ''}
        # check if the email are registered before.
        if len(models.User.objects.filter(email=email)) != 0:
            ret['Info'] = 'User email has been registered， please change a new one.'
            return JsonResponse(ret)
        # obtain unregistered linux user and pwd .
        linux_user_status, linux_user, linux_pwd = get_linux_user_pwd()
        if linux_user_status == 0:
            ret['Info'] = 'linux user register failed'
            models.linuxUser.objects.filter(user=linux_user)[0].used = 0
            return JsonResponse(ret)
        
        email_content = generate_email_content(username, linux_user, linux_pwd)
        # make sure email sending successfully
        send_status = send_email(email, email_content)
        if send_status == 0:
            models.linuxUser.objects.filter(user=linux_user)[0].used = 0
            ret['Info'] = 'Email sending error, please make sure the email can be linked.'
            return JsonResponse(ret)

        # 实例化用户，然后赋值
        user = models.User()
        user.username = username
        user.studentId = studentId
        user.email = email
        user.linuxUser = linux_user
        user.linuxPwd = linux_pwd
        user.save()
        ret['status'] =1
        return JsonResponse(ret)