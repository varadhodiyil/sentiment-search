# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=100, blank=True, null=True)
    display_picture = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=250,null=False)
    password = models.CharField(max_length=60,null=False)
    class Meta:
        db_table = 'users'