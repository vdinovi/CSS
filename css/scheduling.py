from django.http import HttpResponse, HttpResponseRedirect
from .models import Course, CUser, Room, Schedule
from .forms import AddScheduleForm
import json
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

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
                res.status_code = 400
                res.reason_phrase = "NYI"
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




