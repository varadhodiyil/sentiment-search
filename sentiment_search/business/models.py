from __future__ import unicode_literals

from django.db import models

class Business(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=100, blank=True, null=True)
    logo = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=250,null=False)
    password = models.CharField(max_length=60,null=False)
    class Meta:
        db_table = 'business'


class TopicData(models.Model):
    id = models.CharField(primary_key=True, max_length=60)
    topic_key = models.IntegerField()
    data_entry = models.TextField()
    platform = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    sentiment_x = models.DecimalField(max_digits=7, decimal_places=5)
    sentiment_y = models.DecimalField(max_digits=7, decimal_places=5)
    created_by = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=50, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    likes_fav = models.IntegerField(blank=True, null=True)
    shares_retweet = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'topic_data'
        managed = False
        db_tablespace = 'test_sentiment'


class TopicKeys(models.Model):
    id = models.AutoField(primary_key=True)
    key_val = models.CharField(max_length=255)
    topic_type = models.CharField(max_length=30)

    class Meta:
        db_tablespace = 'test_sentiment'
        db_table = 'topic_keys'



class Logs(models.Model):
    log_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    event = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'logs'
        db_tablespace = 'default'

