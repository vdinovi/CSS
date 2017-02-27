from django.http import HttpResponse
from .models import Course, CUser, Room, Schedule
import json

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
    else:
        res.status_code = 400 
    return res


# A function to detect conflicts when creating a new section.
#
# Function is called when creation of a new section is requested.
#
# Updates sections with conflicts to a 'y' in conflicts and updates
# the conflict reason.

# def Conflicts(request):