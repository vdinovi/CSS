from django.template import Context, Template, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from MySQLdb import *
from django.db import IntegrityError
from .models import *
from .forms import *
from settings import DEPARTMENT_SETTINGS
from json import *
from collections import OrderedDict

# ------ UTIL -----
def ErrorView(request, code, reason):
    return render(request, 'error.html', {
                    'code': code,
                    'reason': reason
                  })

# ---------------------------
# --  Method-Based Views   --
# ---------------------------
def RegistrationView(request):
    res = HttpResponse()
    if request.method == "GET":
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        user_type = request.GET.get('user_type')
        email =  request.GET.get('email')
        if first_name is None or last_name is None or user_type is None or email is None:
            return ErrorView(request, 400, "Please visit from the emailed registration link")
        else:
            storage = messages.get_messages(request)
            for msg in storage:
                pass
            return render(request, 'registration.html', {
                'registration_form': RegisterUserForm(request="GET",
                    first_name=first_name,
                    last_name=last_name,
                    user_type=user_type,
                    email=email)
                });
    elif request.method == "POST":
        form = RegisterUserForm(request.POST, request="POST")
        if form.is_valid():
            try:
                user = form.save()
                return HttpResponseRedirect("/home")
            # db error
            except ValidationError as e:
                if re.search(r'duplicate', e[0]):
                    return ErrorView(request, 400, "A user with that name already exists. Please login if that's you or contact a department scheduler.")
                else:
                    return ErrorView(request, 500, "Validation Error:" + e[0])
            except IntegrityError as e:
                if re.search(r'duplicate', e[0]):
                    return ErrorView(request, 400, "A user with that email already exists. Please login if that's you or contact a department scheduler.")
                else:
                    return ErrorView(request, 500, "DB Error:" + e[0])
        else:
            return ErrorView(request, 400, "Invalid form entry")
    else:
        return ErrorView(request, 400, "")
    return res

#  Index View
# @descr This is the splash page that all unauthorized users will get when visitng our base url.
# @TODO  Figure out what to put on this page (so far: FAQ, Feedback, UserManual links)
# @update 1/31/17
def IndexView(request):
    return render(request, 'index.html')

#  Home View
# @descr The view that logged in users will see and will contain their control panel.
#        Will have a different control panel based on the authenticated user.
# @TODO  Add control panel for scheduler first, then add mechanism for loading based on usertype,
#        then add control panel for faculty.
# @update 1/31/17
def HomeView(request):
    return render(request, 'home.html')

def CoursePreferences(request):
	res = HttpResponse()
	faculty = CUser.get_faculty(email = request.session.get('email'))
	if request.method == "GET":
		return render(request,'course_prefs.html', {'add_course_pref': CoursePrefForm()})
	elif request.method == "POST" and 'add_course_pref' in request.POST:
		print('here')
		form = CoursePrefForm(request.POST)
		if form.is_valid():
			try:
				form.save(faculty)
				return HttpResponseRedirect('/course')
			except ValidationError as e:
				return ErrorView(request, 400, "Invalid form entry")
			else:
				return ErrorView(request, 400, "Invalid form entry")
	else:
		print('form not valid')
		return ErrorView(request, 400, "")
	return res

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def AvailabilityView(request):
    res = HttpResponse()
    email = request.session.get('email')
    availability = Availability.get_availability(CUser.get_faculty(email=email))
    print "Availability"
    print Availability.objects.count()

    if request.method == "GET":
        return render(request,'availability.html', {
        			'availability': availability,
                    'add_availability_form': AddAvailabilityForm()})
    elif request.method == "POST" and 'add_availability_form' in request.POST:
        form = AddAvailabilityForm(request.POST)
        if form.is_valid():
            try:
                form.save(email)
                return HttpResponseRedirect('/availability')
            except ValidationError as e:
            	print('form cannot save')
            	print(request.POST.get('level'))
                return ErrorView(request, 400, "Invalid form entry")
        else:
            return ErrorView(request, 400, "Invalid form entry")
    else:
        return ErrorView(request, 400, "")
    return res


def SchedulingView(request):
    res = HttpResponse()
    if request.method == "GET":
        return render(request, 'scheduling.html', {
                      'academic_terms': Schedule.objects.filter().all(),
                      'courses': Course.objects.filter().all(),
                      'section_types': SectionType.objects.filter().all(),
                      'faculty': CUser.get_all_faculty(),
                      'rooms': Room.objects.filter().all(),
                      'add_section_form': AddSectionForm(),
                      'add_schedule_form': AddScheduleForm()
                      })
    else:
        return ErrorView(request, 400, "")
    return res

def LandingView(request):
    return render(request,'landing.html')

def SettingsView(request):
    res = HttpResponse()
    if request.method == "GET":
        return render(request, 'settings.html', {
                'settings': DEPARTMENT_SETTINGS,
                'section_type_list': SectionType.objects.filter().all(),
                'add_section_type_form': AddSectionTypeForm(),
                'upload_form': UploadForm(),
            });
    elif request.method == "POST" and "submit-settings" in request.POST:
        try:
            DEPARTMENT_SETTINGS.new_settings(chair=request.POST['chair'],
                                             name=request.POST['name'],
                                             start_time=request.POST['start_time'],
                                             end_time=request.POST['end_time'])
            return HttpResponseRedirect('/department/settings')
        except ValidationError as e:
            return ErrorView(request, 400, e[0])
        else:
            return ErrorView(request, 400, "Invalid form entry")
    elif request.method == "POST" and "add-section-type" in request.POST:
        form = AddSectionTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/department/settings')
        else:
            return ErrorView(request, 400, "Invalid form entry")
    elif request.method == "POST" and "delete-section-type" in request.POST:
        section = SectionType.get_section_type(name=request.POST['section-type-name'])
        if section is not None:
            section.delete()
            return HttpResponseRedirect('/department/settings')
        else:
            return ErrorView(request, 400, "SectionType " + request.POST['section-type-name'] + " does not exist")
    elif request.method == "POST" and 'file-upload' in request.POST:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                filetype = request.POST.get('filetype')
                result = None
                if filetype == "Student Plan Data":
                    result = StudentPlanData.import_student_plan_file(request.FILES['file'])
                elif filetype == "Cohort Data":
                    result = CohortData.import_cohort_file(request.FILES['file'])
                elif filetype == "Historic Enrollment Data":
                    #@TODO implement
                    #result = StudentPlanData.import_student_plan_file(request.FILES['file'])
                    result = ["Historic Data File Parsing: NOT YET IMPLEMENTED"]
                else:
                    return ErrorView(request, 400, "Invalid form entry")
                for m in result:
                    messages.add_message(request, messages.ERROR, m, extra_tags="cohort")
                return HttpResponseRedirect("/department/settings")
            except:
                raise
            return ErrorView(request, 500, "Failed upload")
        else:
            return ErrorView(request, 400, "Invalid form entry")
    else:
        return ErrorView(request, 400, "")
    return res

from .forms import LoginForm
from django.contrib.auth import authenticate
def LoginView(request):
    res = HttpResponse()
    if request.method == "GET":
        storage = messages.get_messages(request)
        for msg in storage:
            pass
        return render(request, 'login.html', {'login_form':LoginForm()})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            # Authentication success
            if user is not None:
                login(request,user)
                cuser = CUser.objects.get(user=user)
                request.session['user_id'] = user.id
                request.session['email'] = user.username
                request.session['user_type'] = cuser.user_type
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                request.session.set_expiry(6000) # 5 min session duration
                return HttpResponseRedirect('/home')
            # Authentication failed
            else:
                messages.error(request, "Invalid login credentials. Please try again.")
                return render(request,'login.html', {'login_form':LoginForm(),'errors': messages.get_messages(request)})
        else:
            return ErrorView(request, 400, "")
    else:
        return ErrorView(request, 400, "")
    return res


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect('/login')

#  Rooms View
# @descr
# @update 2/2/17
def RoomsView(request):
    res = HttpResponse()
    if request.method == "GET":
        return render(request, 'rooms.html', {
                'room_list': Room.objects.filter(),
                'add_room_form': AddRoomForm(),
                'delete_room_form': DeleteRoomForm(),
                'edit_room_form': EditRoomForm(auto_id='edit_room_%s')
            });
    elif request.method == "POST" and 'add-form' in request.POST:
        form = AddRoomForm(request.POST)
        if form.is_valid():
            try:
                form.save();
                return HttpResponseRedirect("/resources/rooms")
            except ValidationError as e:
                return ErrorView(request, 400, "Invalid form entry")
            except IntegrityError as e:
                if not e[0] == 1062:
                    return ErrorView(request, 500, e[0])
                else:
                    return ErrorView(request, 400, "Duplicate Entry")
        else:
            return ErrorView(request, 400, "Invalid form entry")
    elif request.method == "POST" and 'edit-form' in request.POST:
        form = EditRoomForm(request.POST)
        if form.is_valid():
            form.save()
            res.status_code = 200
            return HttpResponseRedirect('/resources/rooms')
        else:
            return ErrorView(request, 400, "")
    elif request.method == "POST" and 'delete-form' in request.POST:
        form = DeleteRoomForm(request.POST)
        if form.is_valid():
            form.deleteRoom()
            res.status_code = 200
            return HttpResponseRedirect('/resources/rooms')
        else:
            return ErrorView(request, 400, "")
    else:
        return ErrorView(request, 400, "")
    return res

#  Courses View
# @descr
# @update 2/5/17
from .models import Course
from .forms import AddCourseForm
def CoursesView(request):
    res = HttpResponse()
    if request.method == "GET":
        return render(request, 'courses.html', {
                'course_list': Course.objects.filter(),
                'add_course_form': AddCourseForm(auto_id='add_course_%s'),
                'edit_course_form': EditCourseForm(auto_id='edit_course_%s'),
                'delete_course_form': DeleteCourseForm(),
                'add_course_section_type_form': AddCourseSectionTypeForm(),
		'upload_form': UploadForm()
            });
    elif request.method == "POST" and 'add-course-form' in request.POST:
        form = AddCourseForm(request.POST);
        if form.is_valid():
            try:
                form.save();
                return HttpResponseRedirect("/resources/courses")
            except ValidationError as e:
                return ErrorView(request, 400, "Invalid form entry")
            except IntegrityError as e:
                if not e[0] == 1062:
                    return ErrorView(request, 400, e[0])
                else:
                    return ErrorView(request, 400, "Duplicate Entry")
        else:
            return ErrorView(request, 400, "Invalid form entry")
    elif request.method == "POST" and 'edit-course-form' in request.POST:
        form = EditCourseForm(request.POST)
        if form.is_valid():
            form.save()
            res.status_code = 200
            return HttpResponseRedirect('/resources/courses')
        else:
            return ErrorView(request, 400, "Invalid form entry")
    elif request.method == "POST" and 'delete-course-form' in request.POST:
        form = DeleteCourseForm(request.POST)
        if form.is_valid():
            form.save()
            res.status_code = 200
            return HttpResponseRedirect('/resources/courses')
        else:
            return ErrorView(request, 400, "Invalid form entry")

    elif request.method == "POST" and 'course-section-request' in request.POST:
        courseName = request.POST.__getitem__('course')
        course = Course.get_course(courseName)
        res.content = course.get_all_section_types_JSON()

    elif request.method == "POST" and 'delete-section-type-request' in request.POST:
        courseName = request.POST.__getitem__('course')
        sectionTypeName = request.POST.__getitem__('section_type_name')
        course = Course.get_course(courseName)
        course.remove_section_type(sectionTypeName)

        res.content = course.get_all_section_types_JSON()

    elif request.method == "POST" and 'save-section-request' in request.POST:
            courseName = request.POST.__getitem__('course')

            course = Course.get_course(courseName)

            name = request.POST.__getitem__('id_name')
            work_units = request.POST.__getitem__('id_work_units')
            work_hours = request.POST.__getitem__('id_work_hours')

            course.add_section_type(name, work_units, work_hours)

            res.content = course.get_all_section_types_JSON()
    elif request.method == "POST" and 'course-import-data' in request.POST:
	form = UploadForm(request.POST, request.FILES)
	if form.is_valid():
	    try:
		result = Course.import_course_file(request.FILES['file'])
		return HttpResponseRedirect("/resources/courses")
	    except:
		raise
	    res.status_code = 500
	else:
	    res.status_code = 400
	    res.reason_phrase = "Invalid form entry"

    else:
        return ErrorView(request, 400, "")
    return res
#  Schedulers View
# @descr Displays all of the schedulers currecntly registered in the database.
#        Also includes a + and - button that link to the invite form and delete form
# @update 2/4/17
def SchedulersView(request):
    res = HttpResponse()
    if request.method == "GET":
        return render(request, 'schedulers.html', {
                'scheduler_list': CUser.objects.filter(user_type='scheduler'),
                'invite_user_form': InviteUserForm(),
                'delete_user_form': DeleteUserForm()
            });
    elif request.method == "POST" and 'invite-form' in request.POST:
        form = InviteUserForm(request.POST)
        if form.is_valid():
            form.send_invite('scheduler', request)
            return HttpResponseRedirect('/department/schedulers')
        else:
            return ErrorView(request, 400, "")
    elif reqest.method == "POST" and 'edit-form' in request.POST:
        res.status_code = 400
        res.reason_phrase = "NYI"
    elif request.method == "POST" and 'delete-form' in request.POST:
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            try:
                form.delete_user()
                res.status_code = 200
            except ObjectDoesNotExist:
                res.status_code = 404
                res.reason_phrase = "User not found"
        else:
            return ErrorView(request, 400, "Invalid form entry")
    else:
        return ErrorView(request, 400, "")
    return res

#  Faculty View
# @descr Display all of the faculty currently registered in the database.
#        Also includes a + and - button that link to theinvite form and delete form
# @update 2/2/17
def FacultyView(request):
    res = HttpResponse()
    if request.method == "GET":
        return render(request, 'faculty.html', {
                'faculty_list': CUser.objects.filter(user_type='faculty'),
                'invite_user_form': InviteUserForm(),
                'edit_user_form': EditUserForm(auto_id='edit_user_%s'),
                'delete_user_form': DeleteUserForm()
            });
    elif request.method == "POST" and 'invite-form' in request.POST:
        form = InviteUserForm(request.POST)
        if form.is_valid():
            form.send_invite('faculty', request)
            return HttpResponseRedirect('/resources/faculty')
        else:
            return ErrorView(request, 400, "")
    elif request.method == "POST" and 'edit-form' in request.POST:
        form = EditUserForm(request.POST)
        if form.is_valid():
            form.save()
            res.status_code = 200
            return HttpResponseRedirect('/resources/faculty')
        else:
            return ErrorView(request, 400, "Invalid form entry")
    elif request.method == "POST" and 'delete-form' in request.POST:
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            try:
                form.delete_user()
                res.status_code = 200
            except ObjectDoesNotExist:
                res.status_code = 404
                res.reason_phrase = "User not found"
        else:
            return ErrorView(request, 400, "Invalid form entry")

    else:
        return ErrorView(request, 400, "")
    return res


#  FAQ View
# -- Low Priority --
# @descr FAQ view that shows all current FAQ items
# @TODO Create FAQ model and use to populate view
# @Note These FAQ objects could be done without the database
# @update 2/6/17
def FAQView(request):
    res = HttpResponse()
    if request.method == "GET":
        return render(request, 'faq.html', {
                'faq_list': []
            });
    else:
        return ErrorView(request, 400, "")
    return res



# ---------------------------
# --   Class-Based Views   --
# ---------------------------
# @NOTE:Use method-based views for now. They are simpler.
