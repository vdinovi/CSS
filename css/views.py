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

#  Schedulers View
# @descr Displays all of the schedulers currecntly registered in the database.
#        Also includes a + and - button that link to the invite form and delete form
# @TODO Populate list from users in database. Redesign UI with bootstrap.
# @update 2/2/17
def SchedulersView(request):
    return render(request, 'schedulers.html')


#  Invite View 
# @descr Form view enables schedulers to send invites to new users  
#        Form fields are: 'name', 'email', 'UserType'
# @TODO  Should create a URL pointing to the registration page that will be emailed to the user.
#        The URL name, email, and usertype embedded in the query string
#        Think about mechanism to prevent faculty from modifying their UserType to scheduler
#        (perhaps send a secret key to faculty only - not the best idea, but it shouldn't matter too much)
# @update 1/31/17
from .forms import InviteForm 
def InviteView(request):
    res = HttpResponse()
    if request.method == "POST":
        invForm = InviteForm(request.POST)
        if (invForm.is_valid()):
            invData = invForm.clean()
            print(invData)
            res.status_code = 200
            res.content = 'Success. <br><br><a href="../../home">Return</a>'
        else:
            print('invalid invite form')
            res = HttpResponse
            res.status_code = 400
            res.reason_phrase = 'Invalid entries: ' #+ [for err in invForm.errors.as_data()]
    elif request.method == "GET":
        inv = InviteForm() 
        return render(request, 'invite.html', {'form': inv})
    else:
        res.status_code = 400
    return res

# ---------------------------
# --   Class-Based Views   --
# ---------------------------
# @NOTE:Use method-based views for now. They are simpler.

