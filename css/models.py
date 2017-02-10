from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

class User(AbstractUser):
    pass

class Room(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256, null=True)
    capacity = models.IntegerField(default=0)
    notes = models.CharField(max_length=1024, null=True)
    equipment = models.CharField(max_length=1024, null=True)

    def get_name(): 
        return self.name

    def get_description():
        return self.description
        
    def get_capacity():
        return self.capacity

    def get_notes():
        return self.notes

    def get_equipment():
        return self.equipment 

class Course(models.Model):
    course_name = models.CharField(max_length=16)
    equipment_req = models.CharField(max_length=2048, null=True)
    description = models.CharField(max_length=2048, null=True)

class FacultyDetails(models.Model):
    # The user_id uses the User ID as a primary key.
    # Whenever this User is deleted, this entry in the table will also be deleted
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
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
    section_type = models.CharField(max_length=32, primary_key=True) # eg. lecture or lab

class FacultyWorkInfo(models.Model):
    class Meta:
        unique_together = (("course_id", "section_type"),)
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)
    section_type = models.ForeignKey(SectionType, on_delete = models.CASCADE)
    work_units = models.IntegerField(default = 0)
    work_hours = models.IntegerField(default = 0)
