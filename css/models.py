from django.db import models

class User(models.Model):
   username = models.CharField(max_length=32)
   user_type = models.CharField(max_length=16)   # e.g. scheduler, faculty
   email = models.CharField(max_length=32)
   password = models.CharField(max_length=128)
   salt = models.CharField(max_length=128)
   first_name = models.CharField(max_length=16)
   last_name = models.CharField(max_length=16)

class Room(models.Model):
   name = models.CharField(max_length=32)
   description = models.CharField(max_length=256, null=True)
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
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    target_workload = models.IntegerField() # in hours
    changed_preferences = models.CharField(max_length=1) # 'y' or 'n' 

class Schedule(models.Model):
    academic_term = models.CharField(max_length=16, unique=True) # eg. "Fall 2016"
    state = models.CharField(max_length=16) # eg. active or finalized 

class Section(models.Model):
    schedule_id = models.OneToOneField(Schedule, on_delete=models.CASCADE, unique=True)
    course_id = models.OneToOneField(Course, on_delete=models.CASCADE, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.CharField(max_length = 8)    # MWF or TR
    faculty = models.OneToOneField(User, null = True, on_delete = models.SET_NULL, default = models.SET_NULL)
    room = models.OneToOneField(Room, null = True, on_delete = models.SET_NULL, default = models.SET_NULL)
    section_capacity = models.IntegerField(default = 0)
    students_enrolled = models.IntegerField(default = 0)
    students_waitlisted = models.IntegerField(default = 0)
    conflict = models.CharField(max_length = 1)  # y or n
    conflict_reason = models.CharField(max_length = 8) # faculty or room
    fault = models.CharField(max_length = 1) # y or n
    fault_reason = models.CharField(max_length = 8) # faculty or room

class SectionType(models.Model):
    section_type = models.CharField(max_length=32) # eg. lecture or lab
