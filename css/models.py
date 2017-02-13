from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.conf import settings
import MySQLdb
import re
from django.db import IntegrityError
from django.core.exceptions import ValidationError

# ---------- User Models ----------

# CUserManager defines functions for creating and managing CUser objects
class CUserManager(models.Manager):
    # Verify email is valid
    def validate_email(self, email): 
        if re.match(r'^[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}$',
                    email) is None:
            raise ValidationError("Attempted CUser creation"+ 
                                  "with invalid email address")
        return email

    # Password must:
    #   be 8-32 chars, have 1 alphabetical char, 1 digit,
    #   and 1 special char[$@!%*#?&]
    # @TODO Combine independent regex checks
    def validate_password(self, password):
        matches = []
        matches.append(re.match(r'[A-Za-z]+', password))
        matches.append(re.match(r'[0-9]+', password))
        matches.append(re.match(r'[#?!@$%^&*-]+', password))
        if len(password) < 8 or len(password) > 32 or matches is None:
            raise ValidationError("Attempted CUser creation with invalid password")
        return password

    # Verify user_type is either 'scheduler' or 'faculty'
    def validate_user_type(self, user_type):
        if user_type != 'scheduler' and user_type != 'faculty':
            raise ValidationError("Attempted CUser creation with invalid user_type")
        return user_type

    def create_cuser(self, email, password, user_type):
        user = self.create(user=User.objects.create_user(
                               username=self.validate_email(email), 
                               email=self.validate_email(email),
                               password=self.validate_password(password)),
                           user_type=self.validate_user_type(user_type))
        return user

    def get_faculty(self, email=None):
        # Get all faculty
        if email is None:
            return self.filter(user_type='faculty')
        # Faculty with specified email
        else:
            return self.filter(user_type='faculty', user__username=email)


    def get_scheduler(self, email=None):
        # Get all schedulers
        if email is None:
            return self.filter(user_type='scheduler')
        # Scheduler with specified email
        else:
            return self.filter(user_type='scheduler', user__username=email)

class CUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_type = models.CharField(max_length=16)

    objects = CUserManager()

    def delete(self):
        self.user.delete()
        super(CUser, self).delete()

 
class FacultyDetails(models.Model):
    # The user_id uses the User ID as a primary key.
    # Whenever this User is deleted, this entry in the table will also be deleted
    user = models.OneToOneField(CUser, on_delete=models.CASCADE, blank=False)
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

   def validate_name(name):
      if name.length > 32:
         raise ValidationError("Room name is longer than 32 characters")

   def validate_description(description):
      if description.length > 256:
         raise ValidationError("Room description is longer than 256 characters")
   
   def validate_notes(notes):
      if notes.length > 1024:
         raise ValidationError("Room notes is longer than 1024 characters")
   
   def validate_description(description):
      if description.length > 256:
         raise ValidationError("Room description is longer than 256 characters")



# Course represents a department course offering
class Course(models.Model):
    course_name = models.CharField(max_length=16)
    equipment_req = models.CharField(max_length=2048, null=True)
    description = models.CharField(max_length=2048, null=True)

    @classmethod
    def create(cls, course_name, equipment_req, description):
        # try:
        #     course = cls(course_name=course_name, 
        #                  equipment_req=equipment_req, 
        #                  description=description)
        # except Error as e:
        #     raise ValidationError("Invalid data for course creation.")
        # return course

        course = cls(course_name=course_name, 
                         equipment_req=equipment_req, 
                         description=description)
        return course

class SectionType(models.Model):
    section_type = models.CharField(max_length=32) # eg. lecture or lab

    @classmethod
    def create(cls, section_type_name):
        if len(section_type_name) > 32:
            raise ValidationError("Section Type name exceeds 32 characters.")
        else:
            return cls(section_type = section_type_name)


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
        unique_together = (("faculty_id", "days_of_week", "start_time"),)
    faculty_id = models.OneToOneField(WorkInfo, on_delete=models.CASCADE) #
    days_of_week = models.CharField(max_length=16) # MWF or TR
    start_time = models.TimeField()
    end_time = models.TimeField()
    level = models.CharField(max_length=16) # unavailable, preferred, unavailable

    

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