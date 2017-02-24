from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.conf import settings
import MySQLdb
import re
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from util import DepartmentSettings
from settings import DEPARTMENT_SETTINGS

# System User class,
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
        try:
            user = cls(user=User.objects.create_user(username=cls.validate_email(email), 
                                                     email=cls.validate_email(email),
                                                     password=cls.validate_password(password),
                                                     first_name=cls.validate_first_name(first_name),
                                                     last_name=cls.validate_last_name(last_name)),
                       user_type=cls.validate_user_type(user_type))
            user.save()
            # If user is faculty, create an associated faculty details
            # Target work hours and units are initially 0
            if user_type == 'faculty':
                FacultyDetails.create(user, 0, 0).save()
        except:
            raise
        return user
    # Return cuser by email
    @classmethod
    def get_user(cls, email): # Throws ObjectDoesNotExist
        return cls.objects.get(user__username=email)
    # Return faculty cuser by email
    @classmethod
    def get_faculty(cls, email): # Throws ObjectDoesNotExist
        return cls.objects.get(user__username=email, user_type='faculty')
    # Return all faculty cusers
    @classmethod
    def get_all_faculty(cls): 
        return cls.objects.filter(user_type='faculty')
    # Return scheduler cuser by email
    @classmethod
    def get_scheduler(cls, email): # Throws ObjectDoesNotExist
        return cls.objects.get(user__username=email, user_type='scheduler')
    # Return all scheduler cusers
    @classmethod
    def get_all_schedulers(cls):
        return cls.objects.filter(user_type='scheduler')
    # Set the first name
    @classmethod
    def set_first_name(self, first_name):
        self.first_name = first_name
        self.save()
    # Set the last name
    @classmethod
    def set_last_name(self, last_name):
        self.last_name = last_name
        self.save()
    # Set the password
    @classmethod
    def set_password(self, pword):
        self.password = pword
        self.save()

class FacultyDetails(models.Model):
    # The user_id uses the User ID as a primary key.
    # Whenever this User is deleted, this entry in the table will also be deleted
    faculty = models.OneToOneField(CUser, on_delete=models.CASCADE)
    target_work_units = models.IntegerField(default=0, null=True) # in units
    target_work_hours = models.IntegerField(default=0, null=True) # in hours
    changed_preferences = models.CharField(max_length=1) # 'y' or 'n' 

    @classmethod
    def create(cls, faculty, target_work_units, target_work_hours):
        faculty = cls(faculty=faculty, target_work_units=target_work_units,
                      target_work_hours=target_work_hours, changed_preferences='n')
        faculty.save()
        return faculty

    def change_details(self, new_work_units=None, new_work_hours=None):
        if new_work_units:
            self.target_work_units = new_work_units
        if new_work_hours:
            self.target_work_hours = new_work_hours
        self.changed_preferences = 'y' 

    # @TODO Function to yes changed_preferences to 'n'? Also consider naming it something
    #       more indicative -> preferences_have_changed? has_changed_preferences? etc.

# ---------- Resource Models ----------
# Room represents department rooms
class Room(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=256, null=True)
    capacity = models.IntegerField(default=0)
    notes = models.CharField(max_length=1024, null=True)
    equipment = models.CharField(max_length=1024, null=True)
    
    @classmethod
    def create(cls, name, description, capacity, notes, equipment):
        if name is None:
            raise ValidationError("Room name is required")
        elif len(name) > 32:
            raise ValidationError("Room name is longer than 32 characters")
        elif description and len(description) > 256:
            raise ValidationError("Room description is longer than 256 characters")
        elif notes and len(notes) > 1024:
            raise ValidationError("Room notes is longer than 1024 characters")
        elif equipment and len(equipment) > 256:
            raise ValidationError("Room equipment is longer than 1024 characters")
        else:
            room = cls(name=name, 
                       description=description, 
                       capacity=capacity,
                       notes=notes, 
                       equipment=equipment)
            room.save()
            return room

    @classmethod
    def get_room(cls, name):
        return Room.objects.get(name=name)

# Course represents a department course offering
class Course(models.Model):
    name = models.CharField(max_length=16, unique=True)
    equipment_req = models.CharField(max_length=2048, null=True)
    description = models.CharField(max_length=2048, null=True)

    @classmethod
    def create(cls, name, equipment_req, description):
        try:
            course = cls(name=name, 
                         equipment_req=equipment_req, 
                         description=description)
            course.save()
        except:
            raise ValidationError("Invalid data for course creation.")
        return course
    # Returns all course objects
    @classmethod
    def get_all_courses(cls):
        return cls.objects.filter()

    # Returns course by name
    @classmethod
    def get_course(cls, name):
        return cls.objects.get(name=name)

    # Set the equipment required for this course
    def set_equipment_req(self, equipment_req):
        self.equipment_req = equipment_req
        self.save()

    # Set the description of this course
    def set_description(self, description):
        self.description = description
        self.save()

    # Get all section types associated with this course
    def get_all_section_types(self):
        return WorkInfo.filter(course=self)

    # Get a specific section type associated with this course
    def get_section_type(self, section_type_name): # Throws ObjectDoesNotExist, MultipleObjectsReturned
        section_type = SectionType.get_section_type(section_type_name)
        WorkInfo.objects.get(course=self, section_type=section_type)

    # Associate a new section type with this course
    def add_section_type(self, section_type_name, work_units, work_hours): # Throws ObjectDoesNotExist
        section_type = SectionType.get_section_type(section_type_name)
        WorkInfo.create(self, section_type, work_units, work_hours)


class SectionType(models.Model):
    name = models.CharField(max_length=32, unique=True) # eg. lecture or lab

    @classmethod
    def create(cls, name):
        if len(name) > 32:
            raise ValidationError("Section Type name exceeds 32 characters.")
        else:
            section_type = cls(name=name)
            section_type.save()
            return section_type

    @classmethod
    def get_section_type(cls, name):
        return cls.objects.get(name=name)



# WorkInfo contains the user defined information for specific Course-SectionType pairs
# Each pair has an associated work units and work hours defined by the department
class WorkInfo(models.Model): 
    class Meta:
        unique_together = (("course", "section_type"),)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_type = models.ForeignKey(SectionType, on_delete=models.CASCADE)
    work_units = models.IntegerField(default=0)
    work_hours = models.IntegerField(default=0)

    @classmethod
    def create(cls, course, section_type, work_units, work_hours):
        work_info = cls(course=course, section_type=section_type,
                        work_units=work_units, work_hours=work_hours)
        work_info.save()
        return work_info


class Availability(models.Model):
    class Meta: 
        unique_together = (("faculty", "days_of_week", "start_time"),)
    faculty = models.OneToOneField(CUser, on_delete=models.CASCADE, null=True) 
    days_of_week = models.CharField(max_length=16) # MWF or TR
    start_time = models.TimeField()
    start_type = models.CharField(max_length=2)
    end_time = models.TimeField()
    end_type = models.CharField(max_length=2)
    level = models.CharField(max_length=16) # available, preferred, unavailable

    @classmethod
    def create(cls, email, days, start, s_type, end, e_type, level):
        faculty = CUser.get_faculty(email=email)
        if days is None or len(days) > 16 or (days != "MWF" and days != "TR"):
            raise ValidationError("Invalid days of week input")
        elif (start is None):
            raise ValidationError("Need to input start time")  
        elif (s_type is None):
            raise ValidationError("Need to input start type") 
        elif (end is None):
            raise ValidationError("Need to input end time")
        elif (e_type is None):
            raise ValidationError("Need to input end type") 
        elif (level is None) or (level != "available" and level != "preferred" and level != "unavailable"):
            raise ValidationError("Need to input level of availability: preferred, available, or unavailable")  
        else:
            availability = cls(faculty=faculty, days_of_week=days, start_time=start, start_type=s_type, end_time=end, end_type=e_type, level=level)
            availability.save()
            return availability

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
            schedule = cls(academic_term=academic_term, state=state)
            schedule.save()
            return schedule

    @classmethod
    def get_schedule(cls, term_name):
        return cls.objects.get(academic_term=term_name)


# Section is our systems primary scheduled object
# Each section represents a department section that is planned for a particular schedule
class Section(models.Model):
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, unique=True)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.CharField(max_length=8)    # MWF or TR
    faculty = models.ForeignKey(CUser, null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)
    capacity = models.IntegerField(default=0)
    students_enrolled = models.IntegerField(default=0)
    students_waitlisted = models.IntegerField(default=0)
    conflict = models.CharField(max_length=1, default='n')  # y or n
    conflict_reason = models.CharField(max_length=8, null=True) # faculty or room
    fault = models.CharField(max_length=1, default='n') # y or n
    fault_reason = models.CharField(max_length=8, null=True) # faculty or room

    @classmethod
    def create(
        cls, term_name, course_name, start_time, end_time, days, faculty_email, room_name,
        capacity, students_enrolled, students_waitlisted, conflict, 
        conflict_reason, fault, fault_reason):
        # the schedule and course object will actually be passed into the Section as a OneToOneField
        schedule = Schedule.get_schedule(term_name)
        course = Course.get_course(course_name)
        # the faculty and room will be passed in just as the email and room name (IDs for their models) b/c of the ForeignKey type
        faculty = CUser.get_faculty(faculty_email)
        room = Room.get_room(room_name)
        # if start_time < DEPARTMENT_SETTINGS.start_time:
        #     raise ValidationError("Invalid start time for department.")
        # if end_time > DEPARTMENT_SETTINGS.end_time or end_time < start_time:
        #     raise ValidationError("Invalid end time for department.")
        if days != "MWF" and days != "TR":
            raise ValidationError("Invalid days of the week.")
        if capacity < 0:
            raise ValidationError("Invalid section capacity.")
        if students_enrolled < 0:
            raise ValidationError("Invalid number of enrolled students.")
        if students_waitlisted < 0:
            raise ValidationError("Invalid number of students waitlisted.")
        if conflict != 'y' and conflict != 'n':
            raise ValidationError("Invalid value for conflict.")
        if conflict == 'y' and conflict_reason != "faculty" and conflict_reason != "room":
            raise ValidationError("Invalid conflict reason.")
        if fault != 'y' and fault != 'n':
            raise ValidationError("Invalid value for fault.")
        if fault == 'y' and fault_reason != "faculty" and fault_reason != "room":
            raise ValidationError("Invalid fault reason.")
        section = cls(
                  schedule=schedule, 
                  course=course, 
                  start_time=start_time, 
                  end_time=end_time, 
                  days=days, 
                  faculty=faculty, 
                  room=room,
                  capacity=capacity, 
                  students_enrolled=students_enrolled, 
                  students_waitlisted=students_waitlisted, 
                  conflict=conflict,
                  conflict_reason=conflict_reason, 
                  fault=fault, 
                  fault_reason=fault_reason)
        section.save()
        return section

    @classmethod
    def get_section(cls, **kwargs):
        for k,v in kwargs.iteritems():
            if k == 'schedule':
                return cls.objects.get(schedule=Schedule.get_schedule(v))
            elif k == 'course':
                return cls.objects.get(course=Course.get_course(v))
            elif k == 'faculty':
                return cls.objects.get(faculty=CUser.get_faculty(v))
            elif k == 'room':
                return cls.objects.get(room=Room.get_room(v))
            else:
                return cls.objects.get(k=v)

    """
    # this function takes in a dictionary object of filters that has been serialized from a JSON object based on what the user has selected
    # for filtering by time, it will only take in an array of pairs (an array of 2-piece arrays) so that it will at least have a start time and end time.
    #### there can also be chunks of time, so there are multiple start and end times
    # for any other filter, we will pass on the keyword and array argument as it is to the filter.
    @classmethod 
    def filter(cls, data):
        filter_dict = json.loads(data)
        andSections = cls.objects
        andDict = {}
        orList = []
        prevLogic = ''

        # OR list ex: [('question__contains', 'dinner'), ('question__contains', 'meal'), ('pub_date', datetime.date(2010, 7, 19))]
        # AND dict ex: {'question__contains': 'omelette', 'pub_date' : datetime.date.today()}
        # for key,tags in filter_dict.iteritems():
        #     filters = tags['filters']
        #     if key == "time":
        #         for k,v in filters.iteritems():
        #             if k == "MWF" or k == "TR":
        #                 if 'or' in prevLogic:
                            
        #                     for times in range(len(v)):

        #                 elif 'and' in prevLogic or prevLogic is '':
        #                     andDict.update({'days':k})
        #                     for times in range(len(v)):
        #                         andDict.update({start_time__gte:v[times][0], end_time__lte:v[times][0]})
        #     elif:
        #         # print "   filter(" + key + "=" + ', '.join(filters) + ")"
        #         if 'or' in prevLogic:
        #             # add to List here
        #         elif 'and' in prevLogic or prevLogic is '':
        #             andDict.update({key:filters})

            # if 'or' in prevLogic:
            #     # print("orSections +=")
            #     # orSections += cls.objects.filter()
            # elif 'and' in prevLogic or prevLogic is '':
            #     qList += newQuery
            #     # print("andSections x=")
            #     #andSections = andSections.filter()
            
            # prevLogic = tags['logic'] + " "




        sections = Section.objects
        for key, value in filters.iteritems():
            if key == 'time':
                # START
                # reduce(lambda q, f: q | Q(creator=f), filters, Q())
                sections = sections.filter(reduce(lambda query, filter: query | (Q(start_time >= filter[0]) & Q(end_time <= filter[1])), value, Q()))
                # OR 
                #for pair in value:
                #    sections = sections.filter(start_time >= pair[0]).filter(end_time <= pair[1])
                # END
            else:
                sections = sections.filter(key=value)
    """

class FacultyCoursePreferences(models.Model):
    faculty = models.ForeignKey(CUser, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    rank = models.IntegerField(default = 0)

    @classmethod
    def create(faculty, course, rank):
        course_pref = cls(
            faculty=faculty,
            course=course,
            rank=rank)
        course_pref.save()
        return course_pref

    @classmethod
    def get_faculty_pref(cls, faculty):
        entries = cls.objects.filter(faculty='faculty')
        #join the course ID to the course table
        course_arr = {}
        i = 0
        for entry in entries:
            course_id = entry.value(course)
            #course_obj holds the entry in the table in the course table
            course_obj = Course.objects.get(id=course_id)
            course_arr[course_obj.rank] = course_obj.course_name
        course_arr.sort()
        return course_arr.values()
