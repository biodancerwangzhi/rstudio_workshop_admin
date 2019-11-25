from django.db import models

class User(models.Model):
    username = models.TextField()
    studentId = models.TextField()  
    email = models.TextField()
    linuxUser = models.TextField()
    linuxPwd = models.TextField()

class linuxUser(models.Model):
    user = models.TextField()
    password = models.TextField()
    used = models.IntegerField()
