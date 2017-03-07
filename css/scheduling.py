from django.http import HttpResponse, HttpResponseRedirect
from .models import Course, CUser, Room, Schedule, Section, SectionConflict, StudentPlanData, CohortData, CohortTotal
from .forms import AddScheduleForm
import json
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core import serializers
from .settings import DEPARTMENT_SETTINGS
from django.db.models import Q
from datetime import datetime, time

# Used to retrieve options when new filter type is selected
# @NOTE 'Options' refers to specific Courses, Faculty, Rooms, or Time periods
# Responds with a JSON object of the following form:
# {
#   "options": [...]
# }
def Options(request):
    res = HttpResponse()
    if request.method == "GET":
        option_type = request.GET.get('type') 
        if option_type is None:
            res.status_code = 400
            res.reason_phrase = "Missing option type"
        else:
            res.content_type = "application/json"
            if option_type == "Course":
                data = json.dumps({"options": [x.to_json() for x in Course.get_all_courses().all()] })
                res.write(data)
                res.status_code = 200
            elif option_type == "Faculty":
                data = json.dumps({"options": [x.to_json() for x in CUser.get_all_faculty().all()] })
                res.write(data)
                res.status_code = 200
            elif option_type == "Room":
                data = json.dumps({"options": [x.to_json() for x in Room.get_all_rooms().all()] })
                res.write(data)
                res.status_code = 200
            elif option_type == "Time":
                data = json.dumps({'start_time': DEPARTMENT_SETTINGS.start_time, 
                                  'end_time': DEPARTMENT_SETTINGS.end_time});
                res.write(data)
                res.status_code = 200
            else:
                res.status_code = 400
                res.reason_phrase = "Missing option type"
    else:
        res.status_code = 400 
    return res

# Used to retreive schedules
# Responds with a JSON object of the following form:
# @TODO for now, all schedules are being delivered as active
# {
#   "approved": [...],
#   "active": [...],
#   "old": [...]
# }
def Schedules(request):
    res = HttpResponse()
    if request.method == "GET":
        res.content_type = "application/json"
        data = json.dumps({"active": [x.to_json() for x in Schedule.get_all_schedules().all()] })     
        res.write(data)
        res.status_code = 200
    elif request.method == "POST" and "approve-schedule" in request.POST:
        try:
            academic_term = request.POST.get('academic-term') 
            Schedule.get_schedule(term_name=academic_term).approve()
            return HttpResponseRedirect('/scheduling')
        except IntegrityError as e:
            if not e[0] == 1062:
                res.status_code = 500
                res.reason_phrase = "db error:" + e[0]
            else:
                res.status_code = 400
                res.reason_phrase = "Duplicate entry"
        except:
            res.status_code = 400
    elif request.method == "POST" and "add-schedule" in request.POST:
        form = AddScheduleForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/scheduling')
            except ObjectDoesNotExist:
                res.status_code = 404
                res.reason_phrase = "Schedule not found"
            except IntegrityError as e:
                res.status_code = 500
                res.reason_phrase = e[0]
        else:
            res.status_code = 400
            res.reason_phrase = "Invalid form entry" 
    elif request.method == "POST" and "delete-schedule" in request.POST:
        try:
            academic_term = request.POST.get('academic-term') 
            Schedule.get_schedule(term_name=academic_term).delete()
            return HttpResponseRedirect('/scheduling')
        except ObjectDoesNotExist:
            res.status_code = 404
            res.reason_phrase = "Schedule not found"
        except:
            res.status_code = 400
            res.reason_phrase = "Invalid form entry" 
    else:
        res.status_code = 400 
    return res

# Used to retrieve sections when apply button is selected
# @NOTE 'Sections' refers to the sections that match the filters set in  
# Responds with a JSON object of the following form:
# {
#   "sections": [...]
# }
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def Sections(request):
    res = HttpResponse()
    if request.method == "POST":  
        sections = Section.filter_json(request.body)
        res.write(json.dumps({"sections":[sect.to_json() for sect in sections]}))
        res.status_code = 200
    else:
        res.status_code = 400 
    return res

# Creating a new section.
@csrf_exempt
def NewSection(request):
    res = HttpResponse()
    if request.method == "POST":
        sectionData = json.loads(request.body)
        Section.create(
                sectionData['section_num'],
                sectionData['schedule'],
                sectionData['course'],
                sectionData['section-type'],
                sectionData['start-time'],
                sectionData['end-time'],
                sectionData['days'],
                sectionData['faculty'],
                sectionData['room'],
                sectionData['capacity'],
                0, 
                0,
                'n',
                None,
                'n',
                None
                )
        res.status_code = 200
        res.write(request.body)
    else:
        res.status_code = 400
    return res

# Editing a section
@csrf_exempt
def EditSection(request):
    res = HttpResponse()
    if request.method == "POST":
        sectionName = json.loads(request.body)['section']
        section = Section.get_section_by_name(sectionName)
        section_info = {'options': {
                            'section-type': SectionType.objects.filter().all(),
                            'faculty': CUser.get_all_faculty(),
                            'room': Room.objects.filter().all(), 
                        }, 
                        'info': {
                            'section-num': section.section_num,
                            'section-type': section.section_type,
                            'faculty': section.faculty.user.first_name + " " +  section.faculty.user.last_name,
                            'room': section.room.name,
                            'capacity': section.capacity,
                            'students-enrolled': section.students_enrolled, 
                            'students-waitlisted': section.students_waitlisted,
                            'days': section.days,
                            'start-time': section.start_time, 
                            'end_time': section.end_time
                        }}
        res.content_type = "application/json"
        data = json.dumps(section_info)     
        res.write(data)
        res.status_code = 200
    # elif request.method == "POST":
    #     section_info = json.loads(request.body)
    #     section = Section.get_section_by_name(section_info['name'])
    #     section.update(schedule=section_info['term'],
    #                     capacity=section_info['capacity'], 
    #                     students_waitlisted=section_info['num_waitlisted'],
    #                     students_enrolled=section_info['num_enrolled'], 
    #                     start_time=section_info['start_time'],  
    #                     end_time=section_info['end_time'],  
    #                     days=section_info['days'], 
    #                     room=section_info['room'], 
    #                     section_type=section_info['days']
    #                     )
### Can edit everything besides the section number, the course, and the term 

# Deleting a section.
@csrf_exempt
def DeleteSection(request):
    res = HttpResponse()
    if request.method == "POST":
        # sectionName = json.loads(request.body)["section"]
        # sectionObject = Section.get_section_by_name(sectionName)
        # sectionObject.delete()
        res.content_type = "json"
        res.write(json.dumps({"response":"Success!"}))
        res.status_code = 200
    else:
        res.status_code = 400
    return res


# A function to detect conflicts when creating a new section.
#
# Function is called when creation of a new section is requested.
#
# Updates sections with conflicts to a 'y' in conflicts and updates
# the conflict reason.

def Conflicts(section):
    start_time = datetime.strptime(section.start_time, '%H:%M').time()
    end_time = datetime.strptime(section.end_time, '%H:%M').time()
    room = section.room
    faculty = section.faculty
    academic_term = section.schedule
    room_conflict = False
    faculty_conflict = False

    # Find all sections that are between start_time and end_time of the new section
    # sections = Section.objects.filter(schedule=academic_term).filter(start_time__range=[start_time, end_time]).filter(end_time__range=[start_time, end_time])
    sections = Section.objects.filter(schedule=academic_term).filter(Q(start_time__range=[start_time, end_time]) | Q(end_time__range=[time(start_time.hour, start_time.minute + 1), end_time]))

    # Check if rooms or faculty overlap
    for s in sections:
        if s.room == room:
            s.conflict = 'y'
            s.conflict_reason = 'room'
            s.save()
            if s.id != section.id:
                conflict = SectionConflict.create(section, s, 'room')
                conflict.save()
        if s.faculty == faculty:
            s.conflict = 'y'
            s.conflict_reason = 'faculty'
            s.save()
            if s.id != section.id:
                conflict = SectionConflict.create(section, s, 'faculty')
                conflict.save()

def Conflicts(start_time, end_time, room, faculty, academic_term):
    sections = Section.objects.filter(schedule=academic_term).filter(Q(start_time__range=[start_time, end_time]) | Q(end_time__range=[time(start_time.hour, start_time.minute + 1), end_time]))

    # Check if rooms or faculty overlap
    for s in sections:
        if s.room == room:
            s.conflict = 'y'
            s.conflict_reason = 'room'
            return 
        if s.faculty == faculty:
            s.conflict = 'y'
            s.conflict_reason = 'faculty'
            return 


def GetStudentPlanData(request):
    res = HttpResponse()
    if request.method == "GET":
        try:
            term = request.GET.get('schedule')
            schedule = Schedule.get_schedule(term_name=term)
            student_plan_data = StudentPlanData.get_student_plan_data(schedule=schedule).all()
            data = []
            for _,v in student_plan_data:
               data.append(v.to_json())
            res.write(json.dumps({'data': data}))
        except KeyError as e:
            res.status_code = 400
            if term == None:
                res.reason_phrase = "Missing schedule in query string"
            else:
                res.status_code = 500
        except ObjectDoesNotExist:
            res.status_code = 400
            if schedule is None:
                res.reason_phrase = "Schedule '%s' does not exist" % (request.GET.get('schedule'),)
            elif student_plan_data is None:
                res.reason_phrase = "No student plan data for schedule '%s'" % (schedule.name,)
            else:
                res.status_code = 500
    else:
        res.status_code = 400
    return res

def GetCourseInfo(request):
    res = HttpResponse()
    if request.method == "GET":
        try:
            term = request.GET.get('schedule')
            schedule = Schedule.get_schedule(term_name=term)
            course_name = request.GET.get('course')
            course = Course.get_course(name=course_name)
            cohort_data = CohortData.get_cohort_data(schedule=schedule, course=course).all()
            cohort_total = CohortTotal.get_cohort_total(schedule=schedule).all()
            
            data = {}  
            data['course'] = course.to_json()
            tmp = {}
            for c in cohort_data:
                tmp[c.major] = [
                    c.freshman,
                    c.sophomore,
                    c.junior,
                    c.senior
                ]
            data['cohort_data'] = tmp
            tmp = []
            for c in cohort_total:
                tmp[c.major] = [
                    c.freshman,
                    c.sophomore,
                    c.junior,
                    c.senior
                ]
            data['cohort_total'] = tmp
            res.write(json.dumps(data))
        except KeyError as e:
            res.status_code = 400
            if term is None:
                res.reason_phrase = "Missing schedule in query string"
            elif course is None:
                res.reason_phrase = "Missing course in query string"
            else:
                res.status_code = 500
        except ObjectDoesNotExist:
            res.status_code = 400
            if schedule is None:
                res.reason_phrase = "Schedule '%s' does not exist" % (request.GET.get('schedule'),)
            if course is None:
                res.reason_phrase = "Course '%s' does not exist" % (request.GET.get('course'),)
            elif cohort_data is None or cohort_total is None:
                res.reason_phrase = "No cohort data for schedule '%s' and course '%s'" % (schedule.name, course.name)
            else:
                res.status_code = 500
    else:
        res.status_code = 400
    return res



