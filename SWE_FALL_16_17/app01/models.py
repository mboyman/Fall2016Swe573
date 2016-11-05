from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    gender = models.PositiveIntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    birthday = models.DateField()

class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    activity_type = models.PositiveIntegerField()

class UserActivity(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    pocket = models.TextField()
