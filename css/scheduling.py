from django.http import HttpResponse, HttpResponseRedirect
from .models import Course, CUser, Room, Schedule, Section
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

    # Find all sections that are between start_time and end_time of the new section
    # sections = Section.objects.filter(schedule=academic_term).filter(start_time__range=[start_time, end_time]).filter(end_time__range=[start_time, end_time])
    sections = Section.objects.filter(schedule=academic_term).filter(Q(start_time__range=[start_time, end_time]) | Q(end_time__range=[time(start_time.hour, start_time.minute + 1), end_time]))

    # Check if rooms or faculty overlap
    for s in sections:
        if s.room == room:
            s.conflict = 'y'
            s.conflict_reason = 'room'
            s.save()
        if s.faculty == faculty:
            s.conflict = 'y'
            s.conflict_reason = 'faculty'
            s.save()



