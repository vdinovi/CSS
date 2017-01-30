from django.db import models

class Users(models.Model):
   username = models.CharField(max_length=32)
   userType = models.CharField(max_length=16)   # e.g. scheduler, faculty
   email = models.CharField(max_length=32)
   password = models.CharField(max_length=128)
   salt = models.CharField(max_length=128)
   firstName = models.CharField(max_length=16)
   lastName = models.CharField(max_length=16)

class Rooms(models.Model):
   name = models.CharField(max_length=32)
   description = models.CharField(max-length=256, null=True)
   capacity = models.IntegerField(default=0)
   notes = models.CharField(max_length=1024, null=True)
   equipment = models.CharField(max_length=1024, null=True)
