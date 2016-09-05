# -*- coding: utf-8 -*-
from django.db import models
#from RFSNController import generateepochs
import os, subprocess
from subprocess import Popen, PIPE
class Document(models.Model):
    docfile = models.FileField(upload_to='documents')

class Rfsn(models.Model):
    #nickname = models.CharField(max_length=200,default='node')
    hostname = models.CharField(max_length=500)
    #listenerport = models.CharField(max_length=4,default='5035')
    def scheduleepochs(self, filename):
        string = generateepochs( [ self.hostname ], filename )
        print(string)
        return string

    def isonline(self):
        return True
        """output = subprocess.Popen(["ping", '-c', '1', self.hostname],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE).communicate()
        if (b'unknown' in output[1]):
            return False
        else:
            return True"""

    def setstatus(self, status):
        return "on"
        #if status == "on" or status == "off":
        #    command = "./rfsn_ctl " + hostname + " " + status  
        #    os.system(command)        

    def getstatus(self):
        str = (self.hostname).split('.')
        str[0]  = str[0] + '-rly'
        ip = '.'.join(str) 
        port = '2101'
        path = '/var/www/html/fkhan39/uploadsite/myproject/myapp/relay_cmds/rfsn_ctl'
        stat, stat2 = subprocess.Popen([path, ip, port, 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return stat

    def __str__(self):
        return self.hostname

class Epoch(models.Model):
    rfsn = models.ForeignKey(Rfsn, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField('Specrec launch time')
    unix_jobid = models.IntegerField('Job ID')
    specrec_args = models.CharField(max_length=1000)
    filename = models.CharField(max_length=1000)
    def __str__(self):
        return str(self.rfsn) + ' ' + self.start_datetime + ' ' + self.filename
