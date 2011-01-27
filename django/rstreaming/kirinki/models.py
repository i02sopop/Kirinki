# -*- coding: utf-8 -*-
__license__ = "GNU General Public License, Ver.3"
__author__ = "Pablo Alvarez de Sotomayor Posadillo"

from django.db import models
from django.contrib.auth.models import User
 
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()

class configs(models.Model):
    cfgkey = models.CharField(max_length=50)
    cfgvalue = models.CharField(max_length=200)

    def __unicode__(self):
        return self.cfgkey

class video(models.Model):
    idVideo = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    path = models.CharField(max_length=250)
    format = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published')
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class streaming(models.Model):
    idStreaming = models.AutoField(primary_key=True)
    src = models.IPAddressField(null=True)
    port = models.PositiveIntegerField(null=True)
    mux = models.CharField(max_length=20)
    vMode = models.BooleanField()
    video = models.ForeignKey(video, null=True)
    pid =  models.IntegerField()
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.cfgkey
