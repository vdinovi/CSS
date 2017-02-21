from django.template import Context, Template
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from .models import *
from .forms import *
import MySQLdb


# ---------------------------
# --  Method-Based Views   --
# ---------------------------
def RegistrationView(request):
    res = HttpResponse()

    first_name = request.GET.get('first')
    last_name = request.GET.get('last')
    type = request.GET.get('type')

    #pass these credentials to the RegisterUserForm
    #add arguments to the form

    if request.method == "GET":
        storage = messages.get_messages(request)
        for msg in storage:
            pass
        return render(request, 'registration.html', {
                          'registration_form': RegisterUserForm(first_name,last_name,type)
                      })
    elif request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                #res.status_code = 200
                #return render(request, 'home.html')
                return HttpResponseRedirect("/home")
            except ValidationError as e:
                res.status_code = 400
                res.reason_phrase = "Invalid password entry"
                return HttpResponseRedirect("/register")
            # db error
            except IntegrityError as e:
                if not e[0] == 1062:
                    res.status_code = 500
                    res.reason_phrase = "db error:" + e[0]
                else:
                    res.status_code = 400
                    res.reason_phrase = "Duplicate entry"
                    messages.error(request, "A user with that email already exists. Please login if that's you or contact a department scheduler.")
                    return render(request, 'registration.html', {'registration_form': RegisterUserForm(), 'errors': messages.get_messages(request)})
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

def LandingView(request):
    return render(request,'landing.html')

def SettingsView(request):
    res = HttpResponse()
    if request.method == "GET":
        return render(request, 'settings.html', {
                'section_type_list': SectionType.objects.filter(),
                # 'department_name': DepartmentSettings.objects.filter()
            });
    elif request.method == "POST":
        form = AddCourseForm(request.POST);
        if form.is_valid():
            form.addCourse();
            res.status_code = 200
    return render(request, 'settings.html')

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
            print(user)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/home')
            else:
                messages.error(request, "Invalid login credentials. Please try again.")
                return render(request,'login.html', {'login_form':LoginForm(),'errors': messages.get_messages(request)})
        else:
            res.status_code = 400
    else:
        res.status_code = 400
    return res


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect('/landing')

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
            form.save()
            res.status_code = 200
            return HttpResponseRedirect('/home/rooms')
        else:
            res.status_code = 400
    elif request.method == "POST" and 'edit-form' in request.POST:
        form = EditRoomForm(request.POST)
        if form.is_valid():
            form.save()
            res.status_code = 200
            return HttpResponseRedirect('/home/rooms')
        else:
            res.status_code = 400
    elif request.method == "POST" and 'delete-form' in request.POST:
        form = DeleteRoomForm(request.POST)
        if form.is_valid():
            print request.POST
            form.deleteRoom()
            res.status_code = 200
            return HttpResponseRedirect('/home/rooms')
        else:
            res.status_code = 400
    elif request.method == "POST":
        print request.POST

    else:
        res.status_code = 400
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
            form.send_invite('faculty',request)
            res.status_code = 200
        else:
            print form.errors
            res.status_code = 400
    elif request.method == "POST" and 'edit-form' in request.POST:
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
            res.status_code = 400
            res.reason_phrase = "Invalid form entry"

    else:
        print "didnt even post"
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
