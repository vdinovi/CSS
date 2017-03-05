from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.conf import settings
import MySQLdb
import re
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from util import *
from settings import DEPARTMENT_SETTINGS
import json
import operator
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime


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
    def validate_name(cls, first_name, last_name):
        if first_name and len(first_name) > 30:
            raise ValidationError("Attempted CUser creation with a first_name longer than 30 characters")
        if last_name and len(last_name) > 30:
            raise ValidationError("Attempted CUser creation with a last_name longer than 30 characters")
        if CUser.objects.filter(user__first_name=first_name, user__last_name=last_name).exists():
            raise ValidationError("Attempted CUser creation with duplicate full name.")

    @classmethod
    def create(cls, email, password, user_type, first_name, last_name):
        try:
            cls.validate_name(first_name, last_name)
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
    # Return cuser by full name
    def get_cuser_by_full_name(cls, full_name):
        first_name = full_name.split()[0]
        last_name = full_name.split()[1]
        print first_name + last_name
        return cls.objects.get(user__first_name=first_name,
                               user__last_name=last_name)
    @classmethod
    # Return cuser by full name
    def get_faculty_by_full_name(cls, full_name):
        first_name = full_name.split("-")[0]
        last_name = full_name.split("-")[1]
        print first_name + last_name
        return cls.objects.get(user_type='faculty', user__first_name=first_name,
                               user__last_name=last_name)
    # Return faculty cuser by email
    @classmethod
    def get_faculty(cls, email): # Throws ObjectDoesNotExist
        return cls.objects.get(user__username=email, user_type='faculty')
    # Return all faculty cusers
    @classmethod
    def get_all_faculty(cls):
        return cls.objects.filter(user_type='faculty')
    # Return faculty full name
    @classmethod
    def get_all_faculty_full_name(cls):
        faculty_list = cls.objects.filter(user_type='faculty')
        names_list = []
        for faculty in faculty_list:
            names_list.append('{0} {1}'.format(faculty.user.first_name, faculty.user.last_name))
        return names_list
    # Return scheduler cuser by email
    @classmethod
    def get_scheduler(cls, email): # Throws ObjectDoesNotExist
        return cls.objects.get(user__username=email, user_type='scheduler')
    # Return all scheduler cusers
    @classmethod
    def get_all_schedulers(cls):
        return cls.objects.filter(user_type='scheduler')
    # Return cuser email
    @classmethod
    def get_email(self):
        return self.user.username
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

    def to_json(self):
        return dict(id = self.id,
                    name = self.user.first_name + " " + self.user.last_name,
                    email = self.user.email)


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

    @classmethod
    def get_all_rooms(cls):
        return cls.objects.filter()

    def to_json(self):
        return dict(id = self.id,
                    name = self.name,
                    description = self.description,
                    capacity = self.capacity,
                    notes = self.notes,
                    equipment = self.equipment)

# Course represents a department course offering
class Course(models.Model):
    name = models.CharField(max_length=16, unique=True)
    equipment_req = models.CharField(max_length=2048, null=True)
    description = models.CharField(max_length=2048, null=True)

    @classmethod
    def create(cls, name, equipment_req, description):
        if len(name) > 16:
            raise ValidationError("Name is longer than 16 characters, making it invalid.")
        if len(equipment_req) > 2048:
            raise ValidationError("Description is longer than 2048 characters, making it invalid.")
        if len(description) > 2048:
            raise ValidationError("Description is longer than 2048 characters, making it invalid.")
        course = cls(name=name,
                         equipment_req=equipment_req,
                         description=description)
        course.save()
        return course


    # Returns all course objects
    @classmethod
    def get_all_courses(cls):
        return cls.objects.filter()

    # Returns course by name
    @classmethod
    def get_course(cls, name):
        return cls.objects.get(name=name)

    def to_json(self):
        return dict(id = self.id,
                    name = self.name,
                    equipment_req = self.equipment_req,
                    description = self.description)

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
        return WorkInfo.objects.filter(course=self)

    # Get a specific section type associated with this course
    def get_section_type(self, section_type_name): # Throws ObjectDoesNotExist, MultipleObjectsReturned
        section_type = SectionType.get_section_type(section_type_name)
        return WorkInfo.objects.get(course=self, section_type=section_type)

    # Associate a new section type with this course
    def add_section_type(self, section_type_name, work_units, work_hours): # Throws ObjectDoesNotExist
        section_type = SectionType.get_section_type(section_type_name)
        WorkInfo.create(self, section_type, work_units, work_hours)

    # Remove association between section type and course
    def remove_section_type(self, section_type_name): # Throws ObjectDoesNotExist
        #section_type = SectionType.get_section_type(section_type_name)
        self.get_section_type(section_type_name).delete()
        #WorkInfo.create(self, section_type, work_units, work_hours)

    # Retrieve all section types for this course and format them as JSON
    def get_all_section_types_JSON(self):
        courseSectionTypes = self.get_all_section_types()
        sectionTypesDictionary = {}
        i = 0
        for sectionType in courseSectionTypes:
            sectionTypesDictionary[i] = {
                'course_name': sectionType.course.name,
                'section_type_name': sectionType.section_type.name,
                'work_units': sectionType.work_units,
                'work_hours': sectionType.work_hours
            }
            i+=1
        return JsonResponse(sectionTypesDictionary)


class SectionType(models.Model):
    name = models.CharField(max_length=32, unique=True) # eg. lecture or lab

    @classmethod
    def create(cls, name):
        if len(name) > 32:
            raise ValidationError("Section Type name exceeds 32 characters.")
        section_type = cls(name=name)
        section_type.save()
        return section_type

    @classmethod
    def get_section_type(cls, name):
        return cls.objects.get(name=name)

    @classmethod
    def get_all_section_types(cls):
        return SectionType.objects.all()

    @classmethod
    def get_all_section_types_list(cls):
        list = []
        for sectionType in SectionType.objects.all():
            list.append((sectionType.name, sectionType.name))
        return tuple(list)

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
        unique_together = (("faculty", "day_of_week", "start_time"),)
    faculty = models.ForeignKey(CUser, on_delete=models.CASCADE, null=True)
    day_of_week = models.CharField(max_length=16) # MWF or TR
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    level = models.CharField(max_length=16) #preferred, unavailable

    @classmethod
    def get_availability_list(cls, faculty):
        return cls.objects.filter(faculty=faculty)
	
    @classmethod
    def create(cls, email, day, start_time, end_time, level):
	faculty = CUser.get_faculty(email=email)
        if (day is None):
            raise ValidationError("Invalid days of week input")
        elif (start_time is None):
            raise ValidationError("Need to input start time")
        elif (end_time is None):
            raise ValidationError("Need to input end time")
        elif (level is None) or (level != "preferred" and level != "unavailable"):
            raise ValidationError("Need to input level of availability: preferred or unavailable")
        else:
            availability = cls(faculty=faculty,day_of_week=day, start_time=start_time, end_time=end_time, level=level)
            availability.save()
            return availability

    def to_json(self):
        return dict(faculty = self.faculty,
                    day = self.day_of_week,
                    start_time = self.start_time,
                    end_time = self.end_time,
                    level = self.level)

        # ---------- Scheduling Models ----------
# Schedule is a container for scheduled sections and correponds to exactly 1 academic term
class Schedule(models.Model):
    academic_term = models.CharField(max_length=16, unique=True) # eg. "Fall 2016"
    state = models.CharField(max_length=16, default="active") # eg. active or approved

    def approve(self):
        self.state = "approved"

    def return_to_active(self):
        self.state = "active"

    @classmethod
    def create(cls, academic_term, state):
        if state != "approved" and state != "active" and state != None:
            raise ValidationError("Invalid schedule state.")
        else:
            if state == None:
                state = "active"
            schedule = cls(academic_term=academic_term, state=state)
            schedule.save()
            return schedule

    @classmethod
    def get_schedule(cls, term_name):
        return cls.objects.get(academic_term=term_name)

    @classmethod
    def get_all_schedules(cls):
        return cls.objects.filter();

    @classmethod
    def get_active_schedules(cls):
        return cls.objects.filter(state="active")

    @classmethod
    def get_approved_schedules(cls):
        return cls.objects.filter(state="approved")

    def to_json(self):
        return dict(
                academic_term = self.academic_term,
                state = self.state)



# Section is our systems primary scheduled object
# Each section represents a department section that is planned for a particular schedule
class Section(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_type = models.ForeignKey(SectionType, null=True, on_delete=models.SET_NULL)
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
        cls, term_name, course_name, section_type, start_time, end_time, days, faculty_email, room_name,
        capacity, students_enrolled, students_waitlisted, conflict,
        conflict_reason, fault, fault_reason):
        # these objects will actually be passed into the Section because of the ForeignKey
        schedule = Schedule.get_schedule(term_name)
        course = Course.get_course(course_name)
        section_type = SectionType.get_section_type(section_type)
        faculty = CUser.get_faculty(faculty_email)
        room = Room.get_room(room_name)
        if DEPARTMENT_SETTINGS.start_time and start_time < DEPARTMENT_SETTINGS.start_time:
            raise ValidationError("Invalid start time for department.")
        if DEPARTMENT_SETTINGS.end_time and end_time > DEPARTMENT_SETTINGS.end_time or end_time < start_time:
            raise ValidationError("Invalid end time for department.")
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
                  section_type=section_type,
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

    # this function takes in a dictionary object of filters that has been serialized from a JSON object based on what the user has selected
    # for filtering by time, it will only take in an array of pairs (an array of 2-piece arrays) so that it will at least have a start time and end time.
    #### there can also be chunks of time, so there are multiple start and end times
    # for any other filter, we will pass on the keyword and array argument as it is to the filter.

    @classmethod
    def filter_json(cls, json_string):
        json_stuff = json.loads(json_string)
        return cls.filter(json_stuff)

    @classmethod
    def filter(cls, filter_dict):
        andList = []
        ands = False
        orList = []
        ors = False
        timeList = []
        timeLogicList = []
        timeLogic = ''
        prevLogic = ''
        andQuery = ''
        orQuery = ''
        timeQuery = ''
        finalQuery = ''

        for key,tags in filter_dict.iteritems():
            if 'logic' not in tags or 'filters' not in tags:
                raise ValidationError("JSON not set up correctly. 'logic' and 'filters' are required keys in each filter type.")
            logic = tags['logic']
            filters = tags['filters']
            if key == "time":
                for k,v in filters.iteritems():
                    timeLogic = logic
                    if k == "MWF" or k == "TR":
                        for times in range(len(v)):
                            timeList += [reduce(operator.and_, [Q(days=k), Q(start_time__gte=v[times][0]), Q(end_time__lte=v[times][1])])]
                        if len(timeList) != 0:
                            timeQuery = reduce(operator.or_, timeList)
            else:
                queryLoop = Q()
                for index in range(len(filters)):
                    if key == "course":
                        filterObject = Course.get_course(filters[index])
                        queryLoop = reduce(operator.or_, [queryLoop, Q(course=filterObject)])
                    elif key == "faculty":
                        filterObject = CUser.get_faculty_by_full_name(filters[index])
                        queryLoop = reduce(operator.or_, [queryLoop, Q(faculty=filterObject)])
                    elif key == "room":
                        filterObject = Room.get_room(filters[index])
                        queryLoop = reduce(operator.or_, [queryLoop, Q(room=filterObject)])
                    else:
                        raise ValidationError("Invalid filter type.")

                if 'or' in logic:
                    ors = True
                    orList += [queryLoop]
                elif 'and' in logic or logic is '':
                    ands = True
                    andList += [queryLoop]

        if ands is True:
            andQuery = reduce(operator.and_, andList)
            if (timeQuery != '') and ('and' in timeLogic):
                andQuery = reduce(operator.and_, [andQuery, timeQuery])
            finalQuery = andQuery
        if ors is True:
            orQuery = reduce(operator.and_, orList)
            if (timeQuery != '') and ('or' in timeLogic):
                orQuery = reduce(operator.or_, [orQuery, timeQuery])
            if finalQuery != '':
                finalQuery = reduce(operator.or_, [finalQuery, orQuery])
            else:
                finalQuery = orQuery

        if finalQuery == '':
            finalQuery = timeQuery

        try:
            sections = cls.objects.filter(finalQuery)
        except:
            sections = []
        return sections

    def to_json(self):
        return dict(id = str(self.id),
                    name = self.course.name + "-" + str(self.id),
                    term = self.schedule.academic_term,
                    course = self.course.name,
                    type = self.section_type.name,
                    faculty = self.faculty.user.first_name + " " + self.faculty.user.last_name,
                    room = self.room.name,
                    days = self.days,
                    start_time = self.start_time.strftime("%H:%M%p"),
                    end_time = self.end_time.strftime("%H:%M%p"))


class FacultyCoursePreferences(models.Model):
    faculty = models.ForeignKey(CUser, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    comments = models.CharField(max_length=2048, null=True, default="No comments.")
    rank = models.IntegerField(default = 0)

    @classmethod
    def create(cls, faculty, course, comments, rank):
        course_pref = cls(
            faculty=faculty,
            course=course,
            comments=comments,
            rank=rank)
        course_pref.save()
        return course_pref

    @classmethod
    def get_faculty_pref(cls, faculty):
        entries = cls.objects.filter(faculty=faculty)
        return entries

    @classmethod
    def get_course_list(cls, faculty):
        entries = cls.objects.filter(faculty=faculty)
        # join the course ID to the course table
        course_arr = []
        for entry in entries: # go through and make list of tuples (rank, course_name, course_description, comments)
            course_arr += [(entry.rank, entry.course.name, entry.course.description, entry.comments)]
        course_arr.sort(key=lambda tup:tup[0]) # sort courses by rank (first spot in tuple)
        return course_arr

    def remove(self):
    	# course_list = self.get_course_list(faculty=self.faculty)
    	# for c in course_list:
    	# 	if c.rank > self.rank:
    	# 		c.update(rank = c.rank + 1)
    	self.delete()
    	#return course_list

# Cohort Data as imported from file
class CohortData(models.Model):
    # Composite primary key: [schedule + course + major]
    class Meta:
        unique_together = (("schedule", "course", "major"),)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    major = models.CharField(max_length=8) # Major(CSC, CPE, SE, ...) or TOTAL

    freshman = models.IntegerField(default=0)
    sophomore = models.IntegerField(default=0)
    junior = models.IntegerField(default=0)
    senior = models.IntegerField(default=0)

    @classmethod
    def create(cls, schedule, course, major, **kwargs):
        cohort_entry = cls(schedule=schedule, course=course, major=major)
        if 'freshman' in kwargs:
            cohort_entry.freshman = kwargs['freshman']
        if 'sophomore' in kwargs:
            cohort_entry.sophomore = kwargs['sophomore']
        if 'junior' in kwargs:
            cohort_entry.junior = kwargs['junior']
        if 'senior' in kwargs:
            cohort_entry.senior = kwargs['senior']
        cohort_entry.save()
        return cohort_entry

    @classmethod
    def get_cohort_data(cls, schedule, course, major):
        return cls.objects.get(schedule=schedule, course=course, major=major)

    # Handles an uploaded cohort data file and commits it to the system
    @classmethod
    def import_cohort_file(cls, file): # throws FileParserError
        chunks = []
        for s in file.chunks():
            chunks.append(s)
        data = ''.join(chunks)
        lines = data.split('\n')
        messages = []
        # Read schedule
        term = ''
        for w in lines[0].split():
            term += w + ' '
        term.strip()
        # Get Schedule
        try:
            schedule = Schedule.get_schedule(term_name = term)
        except ObjectDoesNotExist:
            messages.append("Schedule '%s' on line %d does not exist" % (term, i))
            return messages
        # Begin parsing data 
        courses = None
        i = 1
        while i < len(lines):
            # Skip lines until non-empty line or end
            # @TODO Change the re check to look for lines without [A-Za-z0-9]+  (safer)
            while (i < len(lines) and not lines[i].strip()):
                i += 1
            # If done, end
            if i >= len(lines):
                break
            # Else, Process cohort data
            words = lines[i].split()
            major = words[0] # Get major
            # If line continues, create new course array ['Total', 'CPE 101', ... ]
            if len(words) > 1:
                courses = []
                if words[1] != "Total":
                    messages.append("Missing 'Total' index on line %d" % (i,))
                    continue
                for j in range(2, len(words), 2):
                    name = words[j] + ' ' + words[j+1]
                    if not Course.objects.filter(name=name).exists():
                        messages.append("Could not find course '%s' on line %d" % (name, i))
                        return messages
                    else:
                        courses.append(name)
            i += 1
            freshman = lines[i].split()
            sophomore = lines[i+1].split()
            junior = lines[i+2].split()
            senior = lines[i+3].split()
            if (freshman[0] != "Freshman"):
                messages.append("Unexpected keyword '%s', expected 'Freshman' on line %d" % (freshman[0], i))
                continue
            if (sophomore[0] != "Sophomore"):
                messages.append("Unexpected keyword '%s', expected 'Sophomore' on line %d" % (sophomore[0], i))
                continue
            if (junior[0] != "Junior"):
                messages.append("Unexpected keyword '%s', expected 'Junior' on line %d" % (junior[0], i))
                continue
            if (senior[0] != "Senior"):
                messages.append("Unexpected keyword '%s', expected 'Senior' on line %d" % (senior[0], i))
                continue
            # Create cohort total
            for j  in range (1, len(courses)):
                try:
                    if (courses[j] == "Total"):
                        CohortTotal.create(schedule=schedule, major=major, 
                                           freshman=int(freshman[j+1]), sophomore=int(sophomore[j+1]),
                                           junior=int(junior[j+1]), senior=int(senior[j+1]))
                        pass
                    else: 
                        course = Course.get_course(name=courses[j])
                        CohortData.create(schedule=schedule, course=course, major=major,
                                          freshman=int(freshman[j+1]), sophomore=int(sophomore[j+1]),
                                          junior=int(junior[j+1]), senior=int(senior[j+1]))
                        pass
                except ObjectDoesNotExist as e:
                    messages.append("Could not create data entries on lines %d through %d" % (i, i+3))
                except IndexError as e:
                    messages.append("Not enough data entries on lines %d through %d" % (i, i+3))
                except:
                    messages.append("Unkown error on lines %d through %d" % i (i+3))
            i += 4
        return messages

class CohortTotal(models.Model):
    class Meta:
        unique_together =(("schedule", "major"),)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    major = models.CharField(max_length=8) # Major(CSC, CPE, SE, ...)

    freshman = models.IntegerField(default=0)
    sophomore = models.IntegerField(default=0)
    junior = models.IntegerField(default=0)
    senior = models.IntegerField(default=0)

    @classmethod
    def create(cls, schedule, major, **kwargs):
        cohort_total = cls(schedule=schedule, major=major)
        if 'freshman' in kwargs:
            cohort_total.freshman = kwargs['freshman']
        if 'sophomore' in kwargs:
            cohort_total.sophomore = kwargs['sophomore']
        if 'junior' in kwargs:
            cohort_total.junior = kwargs['junior']
        if 'senior' in kwargs:
            cohort_total.senior = kwargs['senior']
        cohort_total.save()
        return cohort_total

    @classmethod
    def get_cohort_total(cls, schedule, major):
        return cls.objects.get(schedule=schedule, major=major)

# Student Plan Data.
class StudentPlanData(models.Model):
    class Meta:
        unique_together = (("schedule", "course", "section_type"),)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_type = models.ForeignKey(SectionType, on_delete=models.CASCADE)

    seat_demand = models.IntegerField(default=0)
    sections_offered = models.IntegerField(default=0)
    enrollment_capacity = models.IntegerField(default=0)
    unmet_seat_demand = models.IntegerField(default=0)
    percent_unmet_seat_demand = models.FloatField(default=0)
    
    @classmethod
    def create(cls, schedule, course, section_type, **kwargs):
        plan_data = cls(schedule=schedule, course=course, section_type=section_type)
        if 'seat_demand' in kwargs:
            plan_data.seat_demand = kwargs['seat_demand']
        if 'sections_offered' in kwargs:
            plan_data.sections_offered = kwargs['sections_offered']
        if 'enrollment_capacity' in kwargs:
            plan_data.enrollment_capacity = kwargs['enrollment_capacity']
        if 'unmet_seat_demand' in kwargs:
            plan_data.unmet_seat_demand = kwargs['unmet_seat_demand']
        if 'percent_unmet_seat_demand' in kwargs:
            plan_data.percent_unmet_seat_demand = kwargs['percent_unmet_seat_demand']
        plan_data.save()
        return plan_data

    @classmethod
    def get_student_plan_data(cls, schedule, course=None, section_type=None):
        if course == None:
            return cls.objects.filter(schedule=schedule)
        if sectionType == None:
            return cls.objects.filter(schedule=schedule, course=course)
        return cls.objects.get(schedule=schedule, course=course, section_type=section_type)

    # Handles an uploaded student plan data file and commits it to the system
    @classmethod
    def import_student_plan_file(cls, file): # throws FileParserError
        chunks = []
        for s in file.chunks():
            chunks.append(s)
        data = ''.join(chunks)
        messages = []
        lines = data.split('\n')
        term_ignore = ["quarter"] #Ignore these terms when reading in term name
        # Keys that are accepted by the system
        valid_keys = ["Term", "Subject Code", "Catalog Nbr", "Course Title", "Component", "Seat Demand",
                      "Sections Offered", "Enrollment Capacity", "Unmet Seat Demand", "% Unmet Seat Demand"] 
        # Index for parsing
        index = lines[0].split(',')
        print "len(index)=" + str(len(index))
        # Null out anything that is not a valid key
        for i in range(0, len(index)):
            if index[i] not in valid_keys: 
                index[i] = None
        # Parse all lines using valid keys in index
        try:
            for i in range(1, len(lines)):
                # Skip any empty lines
                while (i < len(lines) and not lines[i].strip()):
                    i += 1
                # If done, end
                if i >= len(lines):
                    break
                # Parse line
                line = lines[i].split(',')
                content = {} 
                for j in range(0, len(index)):
                    # Does not have a valid key
                    if index[j] is None:
                        continue
                    # Make KV pair with valid key
                    content[index[j]] = line[j]
                # Collect parsed data
                # Remove ignored words from term name
                schedule = Schedule.get_schedule(term_name=' '.join([w for w in content['Term'].split() if w.lower() not in term_ignore]).strip())
                course = None
                section_type = None
                try:
                    course = Course.get_course(name=content['Subject Code']+' '+content['Catalog Nbr'])
                    continue
                except ObjectDoesNotExist:
                    messages.append("Course '%s' on line %d does not exist" % (content['Subject Code']+' '+content['Catalog Nbr'], i))
                try:
                    section_type = SectionType.get_section_type(name=content['Component'])
                except ObjectDoesNotExist:
                    messages.append("Section Type '%s' on line %d does not exist" % (content['Component'], i))
                    continue
                if course and section_type and not course.get_section_type(course=course, section_type=section_type):
                    messages.append("Course '%s' has no associated section type '%s'" % (course.name, section_type.name)) 
                    continue
                already_parsed = ["Term", "Subject Code", "Catalog Nbr", "Component"] 
                # Collect other secondary arguments
                kwargs = {}
                for k, v in content.iteritems():
                    if (v is not None) and (k not in already_parsed):
                        kwargs[k] = v
                # Create entry
                cls.create(schedule=schedule, course=course, section_type=section_type, **kwargs)
                print 'Success'
        except IndexError as e:
            raise FileParserError("Invalid entry on line %d: %s" % (i, e[0]))
        except:
            raise FileParserError("Unknown error on line %d" % (i,))
        return messages
 
# Section Conflicts Model
class SectionConflict(models.Model):
    section1 = models.ForeignKey(Section, related_name="first_section", on_delete=models.CASCADE)
    section2 = models.ForeignKey(Section, related_name="second_section", on_delete=models.CASCADE)
    conflict_reason = models.CharField(max_length=8) # Faculty or Room

    @classmethod
    def create(cls, section1, section2, conflict_reason):
        if section1 == section2:
            raise ValidationError("Section does not conflict with itself.")
        if conflict_reason != "faculty" and conflict_reason != "room":
            raise ValidationError("Invalid conflict reason.")
        conflict = cls(
                    section1=section1, 
                    section2=section2, 
                    conflict_reason=conflict_reason)
        conflict.save()
        return conflict
