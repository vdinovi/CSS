from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group
from django.conf import settings
import re

# ---------- User Models ----------
class CUserManager(BaseUserManager): 
    def create_faculty(self, email, password, first_name=None, last_name=None):
        user = self.create_user(email = email, password = password,
                                first_name = first_name, last_name = last_name,
                                user_type = 'scheduler')
        return user
    
    def create_faculty(self, email, password, first_name=None, last_name=None):
        user = self.create_user(email = email, password = password,
                                first_name = first_name, last_name = last_name,
                                user_type = 'faculty')
        return user

    def create_user(self, email, user_type, password = None, first_name=None, last_name=None):
        if not email or not self.is_email_valid(email):
            raise ValueError('User must have a valid email address')
        user = self.model(email = self.normalize_email(email),
                          first_name = first_name, last_name = last_name,
                          user_type = user_type)
        user.set_password(password)
        user.save()
        return user

    def is_email_valid(email):
        return re.compile("[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}").match(email)


class CUser(AbstractBaseUser):
    email = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    password = models.CharField(max_length=32)
    user_type = models.CharField(max_length=16)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'user_type']

    objects = CUserManager()
    
class FacultyDetails(models.Model):
    # The user_id uses the User ID as a primary key.
    # Whenever this User is deleted, this entry in the table will also be deleted
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target_workload = models.IntegerField() # in hours
    changed_preferences = models.CharField(max_length=1) # 'y' or 'n' 


# ---------- Resource Models ----------
# Room represents department rooms
class Room(models.Model):
   name = models.CharField(max_length=32)
   description = models.CharField(max_length=256, null=True)
   capacity = models.IntegerField(default=0)
   notes = models.CharField(max_length=1024, null=True)
   equipment = models.CharField(max_length=1024, null=True)

# Course represents a department course offering
class Course(models.Model):
    course_name = models.CharField(max_length=16)
    equipment_req = models.CharField(max_length=2048, null=True)
    description = models.CharField(max_length=2048, null=True)

# SectionType contains all the defined section types the department allows
class SectionType(models.Model):
    section_type = models.CharField(max_length=32, primary_key=True) # eg. lecture or lab

# WorkInfo contains the user defined information for specific Course-SectionType pairs
# Each pair has an associated work units and work hours defined by the department
class WorkInfo(models.Model): 
    class Meta:
        unique_together = (("course_id", "section_type"),)
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)
    section_type = models.ForeignKey(SectionType, on_delete = models.CASCADE)
    work_units = models.IntegerField(default = 0)
    work_hours = models.IntegerField(default = 0)

# ---------- Scheduling Models ----------
# Schedule is a container for scheduled sections and correponds to exactly 1 academic term
class Schedule(models.Model):
    academic_term = models.CharField(max_length=16, unique=True) # eg. "Fall 2016"
    state = models.CharField(max_length=16) # eg. active or finalized 

# Section is our systems primary scheduled object
# Each section represents a department section that is planned for a particular schedule
class Section(models.Model):
    schedule_id = models.OneToOneField(Schedule, on_delete=models.CASCADE, unique=True)
    course_id = models.OneToOneField(Course, on_delete=models.CASCADE, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.CharField(max_length = 8)    # MWF or TR
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, on_delete = models.SET_NULL, default = models.SET_NULL)
    room = models.OneToOneField(Room, null = True, on_delete = models.SET_NULL, default = models.SET_NULL)
    section_capacity = models.IntegerField(default = 0)
    students_enrolled = models.IntegerField(default = 0)
    students_waitlisted = models.IntegerField(default = 0)
    conflict = models.CharField(max_length = 1)  # y or n
    conflict_reason = models.CharField(max_length = 8) # faculty or room
    fault = models.CharField(max_length = 1) # y or n
    fault_reason = models.CharField(max_length = 8) # faculty or room

