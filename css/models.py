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

class Course(models.Model):
    course_name = models.CharField(max_length=16)
    equipment_req = models.CharField(max_length=2048, null=True)
    description = models.CharField(max_length=2048, null=True)

class FacultyDetails(models.Model):
    # The user_id uses the User ID as a primary key.
    # Whenever this User is deleted, this entry in the table will also be deleted
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    target_workload = models.IntegerField() # in hours
    changed_preferences = models.CharField(max_length=1) # 'y' or 'n' 

class Schedule(models.Model):
    academic_term = models.CharField(max_length=16, unique=True) # eg. "Fall 2016"
    state = models.CharField(max_length=16) # eg. active or finalized 

class SectionType(models.Model):
    section_type = models.CharField(max_length=32) # eg. lecture or lab
