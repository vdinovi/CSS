from django.template import Context, Template
from django.contrib.auth import authenticate, login
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import *
from .forms import *
import MySQLdb


# ---------------------------
# --  Method-Based Views   --
# ---------------------------
def RegistrationView(request):
    res = HttpResponse()
    if request.method == "GET":
        return render(request, 'registration.html', {
                          'registration_form': RegisterUserForm()
                      })
    elif request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                res.status_code = 200
            # db error
            except MySQLdb.IntegrityError as e:
                if not e[0] == 1062:
                    res.status_code = 500
                    res.reason_phrase = "db error:" + e[0]
                else:
                    res.status_code = 400
                    res.reason_phrase = "Duplicate entry"
        else:
            res.status_code = 400
            res.reason_phrase = "Invalid form entry"
    else:
        res.status_code = 400
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

def SchedulingView(request):
    #@TODO NYI
    return render_to_response('nyi.html')

from .forms import LoginForm
def LoginView(request):
	if request.method == "GET":
		return render(request, 'login.html', {'login_form':LoginForm()});
	elif request.method == "POST":
		form = LoginForm(request.POST)
	return render(request, 'home.html');

#  Rooms View
# @descr
# @TODO
# @update 2/2/17
def RoomsView(request):
    res = HttpResponse()
    if request.method == "GET":
        print("if")
        return render(request, 'rooms.html', {
                'room_list': Room.objects.filter(),
                'add_room_form': AddRoomForm(),
                'delete_room_form': DeleteRoomForm()
            });
    elif request.method == "POST" and 'add-form' in request.POST:
        form = AddRoomForm(request.POST)
        if form.is_valid():
            form.save()
            res.status_code = 200
        else:
            res.status_code = 400
    elif request.method == "POST" and 'delete-form' in request.POST:
        form = DeleteRoomForm(request.POST)
        if form.is_valid():
            print('NYI')
            res.status_code = 200
        else:
            res.status_code = 400
    else:
        res.status_code = 400
    return res

#  Courses View
# @descr
# @TODO
# @update 2/5/17
from .models import Course
from .forms import AddCourseForm
def CoursesView(request):
    res = HttpResponse()
    if request.method == "GET":
        #TODO should filter by those with usertype 'scheduler'
        return render(request, 'courses.html', {
                'course_list': Course.objects.filter(),
                'add_course_form':AddCourseForm()
            });
    elif request.method == "POST":
        form = AddCourseForm(request.POST); 
        if form.is_valid():
            form.addCourse();
            res.status_code = 200
    return render(request, 'courses.html')

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
            form.send_invite('scheduler')
            res.status_code = 200
        else:
            res.status_code = 400
    elif request.method == "POST" and 'delete-form' in request.POST:
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            scheduler = CUser.objects.filter(user__id=form.cleaned_data['id'])
            if scheduler is False:
                res.status_code = 404
                res.reason_phrase = "User with that ID does not exist"
            else:
                scheduler.delete()
                res.status_code = 200

            print('NYI')
            res.status_code = 200
        else:
            res.status_code = 400
    else:
        res.status_code = 400
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
                'delete_user_form': DeleteUserForm()
            });
    elif request.method == "POST" and 'invite-form' in request.POST:
        form = InviteUserForm(request.POST)
        if form.is_valid():
            form.send_invite('faculty')
            res.status_code = 200
        else:
            res.status_code = 400
    elif request.method == "POST" and 'delete-form' in request.POST:
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            faculty = CUser.objects.filter(user__id=form.cleaned_data['id'])
            if faculty is False:
                res.status_code = 404
                res.reason_phrase = "User with that ID does not exist"
            else:
                faculty.delete()
                res.status_code = 200
        else:
            res.status_code = 400
    else:
        res.status_code = 400
    return res

#  FAQ View
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
       res.status_code = 400;
    return res


# ---------------------------
# --   Class-Based Views   --
# ---------------------------
# @NOTE:Use method-based views for now. They are simpler.
