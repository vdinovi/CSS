from django.template import Context, Template
from django.shortcuts import render
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

#  Rooms View
# @descr 
# @TODO 
# @update 2/2/17
def RoomsView(request):
    return render(request, 'rooms.html')


#  Schedulers View
# @descr Displays all of the schedulers currecntly registered in the database.
#        Also includes a + and - button that link to the invite form and delete form
# @TODO Populate list from users in database. Redesign UI with bootstrap.
# @update 2/2/17
def SchedulersView(request):
    return render(request, 'schedulers.html')

#  Faculty View
# @descr Display all of the faculty currently registered in the database.
#        Also includes a + and - button that link to theinvite form and delete form
# @TODO populat lite from users in database. Redesign UI with bootstrap
# @update 2/2/17
from .models import User
from .forms import InviteForm, DeleteForm
def FacultyView(request):
    res = HttpResponse()
    #@TODO should process add faculty and delete faculty form submissions
    if request.method == "POST":
        res.status_code = 400
    elif request.method == "GET":
        return render(request, 'faculty.html', {
            'user_list': User.objects.filter(), #TODO should filter by those with usertype 'faculty'
            'add_faculty_form': InviteForm(),
            'delete_faculty_form': DeleteForm()
            });
    else:
        res.status_code = 400
    return res

# ---------------------------
# --   Class-Based Views   --
# ---------------------------
# @NOTE:Use method-based views for now. They are simpler.

