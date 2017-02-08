from django.template import Context, Template
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponse

# ---------------------------
# --  Method-Based Views   --
# ---------------------------
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

#  Rooms View
# @descr 
# @TODO 
# @update 2/2/17
def RoomsView(request):
    return render(request, 'rooms.html')

#  Courses View
# @descr 
# @TODO 
# @update 2/5/17
def CoursesView(request):
    return render(request, 'courses.html')

#  Schedulers View
# @descr Displays all of the schedulers currecntly registered in the database.
#        Also includes a + and - button that link to the invite form and delete form
# @update 2/4/17
def SchedulersView(request):
    res = HttpResponse()
    if request.method == "GET":
        #TODO should filter by those with usertype 'scheduler'
        return render(request, 'schedulers.html', {
                'scheduler_list': User.objects.filter(), 
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
from .models import User
from .forms import InviteUserForm, DeleteUserForm
def FacultyView(request):
    res = HttpResponse()
    if request.method == "GET":
        #TODO should filter by those with usertype 'faculty'
        return render(request, 'faculty.html', {
                'faculty_list': User.objects.filter(), 
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
            print('NYI')
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

