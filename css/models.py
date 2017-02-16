from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.conf import settings
import MySQLdb
import re
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

# ---------- User Models ----------

# System user class,
# Wrapper for django builtin class, contains user + application specific data
class CUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=16)
    
    @staticmethod
    def validate_email(email): 
        if re.match(r'^[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}$', email) is None:
            raise ValidationError("Attempted CUser creation"+"with invalid email address")
        return email

    # Password must:
    # be 8-32 chars, have: 1 alphachar, 1 digit, 1 specialchar
    @staticmethod
    def validate_password(password):
        if re.match(r'^(?=.*\d)(?=.*[A-Za-z])(?=.*[-._!@#$%^&*?+])[A-Za-z0-9-._!@#$%^&*?+]{8,32}$', password) is None:
            raise ValidationError("Attempted CUser creation with invalid password")
        return password

    @staticmethod
    def validate_user_type(user_type):
        if user_type != 'scheduler' and user_type != 'faculty':
            raise ValidationError("Attempted CUser creation with invalid user_type")
        return user_type

    @staticmethod
    def validate_first_name(first_name):
        if first_name and len(first_name) > 30:
            raise ValidationError("Attempted CUser creation with a first_name longer than 30 characters")
        return first_name

    @staticmethod
    def validate_last_name(last_name):
        if last_name and len(last_name) > 30:
            raise ValidationError("Attempted CUser creation with a last_name longer than 30 characters")
        return last_name

    @classmethod
    def create(cls, email, password, user_type, first_name, last_name):
        user = cls(user=User.objects.create_user(username=cls.validate_email(email), 
                                                 email=cls.validate_email(email),
                                                 password=cls.validate_password(password),
                                                 first_name=first_name,
                                                 last_name=last_name),
                   user_type=cls.validate_user_type(user_type))
        user.save()
        return user
       
    @classmethod
    def get_user(cls, email):
        return cls.objects.get(user__username=email)

    @classmethod
    def get_faculty(cls, email):
        return cls.objects.get(user__username=email, user_type='faculty')

    @classmethod
    def get_all_faculty(cls):
        return cls.objects.filter(user_type='faculty')

    @classmethod
    def get_scheduler(cls, email):
        return cls.objects.get(user__username=email, user_type='scheduler')

    @classmethod
    def get_all_schedulers(cls):
        return cls.objects.filter(user_type='scheduler')
 
    def set_name(self, first, last):
        if first:
            self.user.first_name = first
        if last:
            self.user.last_name = last
        self.user.save()

 
class FacultyDetails(models.Model):
    # The user_id uses the User ID as a primary key.
    # Whenever this User is deleted, this entry in the table will also be deleted
    user = models.OneToOneField(CUser, on_delete=models.CASCADE, blank=False)
    target_workload = models.IntegerField() # in hours
    changed_preferences = models.CharField(max_length=1) # 'y' or 'n' 

    @classmethod
    def create(cls, user, target_workload):
        faculty_details = cls(user=user, target_workload=target_workload,
                              changed_preferences='y')

    def set_changed_preferences(self, changed):
        self.changed_preferences = changed

# ---------- Resource Models ----------
# Room represents department rooms
class Room(models.Model):
   name = models.CharField(max_length=32)
   description = models.CharField(max_length=256, null=True)
   capacity = models.IntegerField(default=0)
   notes = models.CharField(max_length=1024, null=True)
   equipment = models.CharField(max_length=1024, null=True)

   @classmethod
   def create(cls, name, description, cap, notes, equip):
      if name is None:
         raise ValidationError("Room name is required")
      elif len(name) > 32:
         raise ValidationError("Room name is longer than 32 characters")
      elif description and len(description) > 256:
         raise ValidationError("Room description is longer than 256 characters")
      elif notes and len(notes) > 1024:
         raise ValidationError("Room notes is longer than 1024 characters")
      elif equip and len(equip) > 256:
         raise ValidationError("Room equipment is longer than 1024 characters")
      else:
         room = cls(name=name, 
                     description=description, 
                     capacity=cap, notes=notes, 
                     equipment=equip)
         return room



# Course represents a department course offering
class Course(models.Model):
    course_name = models.CharField(max_length=16)
    equipment_req = models.CharField(max_length=2048, null=True)
    description = models.CharField(max_length=2048, null=True)

    @classmethod
    def create(cls, course, equipment, desc):
        try:
            course = cls(course_name = course, 
                         equipment = equipment, 
                         description = desc)
        except:
            raise ValidationError("Invalid data for course creation.")
        return course

class SectionType(models.Model):
    section_type = models.CharField(max_length=32) # eg. lecture or lab

    @classmethod
    def create(cls, section_type_name):
        if len(section_type_name) > 32:
            raise ValidationError("Section Type name exceeds 32 characters.")
        else:
            return cls(section_type = section_type_name)

    @classmethod
    def get_section_type(cls, section_type_name):
        cls.objects.get(section_type_name=section_type_name)


# WorkInfo contains the user defined information for specific Course-SectionType pairs
# Each pair has an associated work units and work hours defined by the department
class WorkInfo(models.Model): 
    class Meta:
        unique_together = (("course", "section_type"),)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_type = models.ForeignKey(SectionType, on_delete=models.CASCADE)
    work_units = models.IntegerField(default=0)
    work_hours = models.IntegerField(default=0)

class Availability(models.Model):
    class Meta: 
        unique_together = (("faculty_member", "days_of_week", "start_time"),)
    faculty_member = models.OneToOneField(CUser, on_delete=models.CASCADE, null=True) 
    days_of_week = models.CharField(max_length=16) # MWF or TR
    start_time = models.TimeField()
    end_time = models.TimeField()
    level = models.CharField(max_length=16) # available, preferred, unavailable

    @classmethod
    def create(cls, email, days, start, end, level):
        faculty = CUser.get_faculty(email=email)
        if days is None or len(days) > 16 or (days != "MWF" and days != "TR"):
            raise ValidationError("Invalid days of week input")
        elif (start is None):
            raise ValidationError("Need to input start time")  
        elif (end is None):
            raise ValidationError("Need to input end time")  
        elif (level is None) or (level != "available" and level != "preferred" and level != "unavailable"):
            raise ValidationError("Need to input level of availability: preferred, available, or unavailable")  
        else:
            return cls(faculty_member=faculty, days_of_week=days, start_time=start, end_time=end, level=level)

# ---------- Scheduling Models ----------
# Schedule is a container for scheduled sections and correponds to exactly 1 academic term
class Schedule(models.Model):
    academic_term = models.CharField(max_length=16, unique=True) # eg. "Fall 2016"
    state = models.CharField(max_length=16, default="active") # eg. active or finalized 

    def finalize_schedule(self):
    	self.state = "finalized"

    def return_to_active(self):
    	self.state = "active"

    @classmethod
    def create(cls, academic_term, state):
        if state != "finalized" and state != "active":
            raise ValidationError("Invalid schedule state.")
        else:
            return cls(academic_term, state)

# Section is our systems primary scheduled object
# Each section represents a department section that is planned for a particular schedule
class Section(models.Model):
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, unique=True)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.CharField(max_length = 8)    # MWF or TR
    faculty = models.ForeignKey(CUser, null = True, on_delete = models.SET_NULL, default = models.SET_NULL)
    room = models.ForeignKey(Room, null = True, on_delete = models.SET_NULL, default = models.SET_NULL)
    section_capacity = models.IntegerField(default = 0)
    students_enrolled = models.IntegerField(default = 0)
    students_waitlisted = models.IntegerField(default = 0)
    conflict = models.CharField(max_length = 1)  # y or n
    conflict_reason = models.CharField(max_length = 8) # faculty or room
    fault = models.CharField(max_length = 1) # y or n
    fault_reason = models.CharField(max_length = 8) # faculty or room
