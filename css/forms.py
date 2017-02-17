from django import forms
from django.core.mail import send_mail
from css.models import CUser, Room
from django.http import HttpResponseRedirect
#from django.contrib.sites.models import Site
import re

#  Login Form
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    #@TODO validate pass?
    @staticmethod
    def validate_password(password):
        pass

#  Invite Form
class InviteUserForm(forms.Form):
    #@TODO Email field not working -> is_valid fails
    #email = forms.EmailField()
    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    #@TODO send registraiton link in email
    def send_invite(self, usertype, request):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        name = first_name + ' ' + last_name
        email = self.cleaned_data['email']
        #your_domain = Site.objects.get_current().domain
        link = 'http://localhost:8000/register?'+first_name + '+' + last_name +'&type='+usertype
        send_mail('Invite to register for CSS',
                  name + """, you have been invited to register for CSS. 
                  Please register using the following link: """ + link,
                  'registration@inviso-css',
                  [self.cleaned_data['email']])

# Registration Form
# @TODO on load, pull fields from query string -> show failure if field not able to be loaded:
#       Fields to pull: email, first_name, last_name, user_type
class RegisterUserForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    user_type = forms.ChoiceField(label='Role', choices=[('faculty', 'faculty'), ('scheduler', 'scheduler')])
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def save(self):
        user = CUser.create(email=self.cleaned_data['email'],
                            password=self.cleaned_data['password2'],
                            user_type=self.cleaned_data['user_type'],
                            first_name=self.cleaned_data['first_name'],
                            last_name=self.cleaned_data['last_name'])
        user.save()
        return user

# Edit User Form
class EditUserForm(forms.Form):
    pass

# Delete Form
class DeleteUserForm(forms.Form):
    email = forms.CharField(label='Confirm email')

    def delete_user(self):
        CUser.get_user(email=self.cleaned_data['email']).delete()

class AddRoomForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    capacity = forms.IntegerField()
    notes = forms.CharField()
    equipment = forms.CharField()

    def save(self):
		print "save"
		nameString = self.cleaned_data['roomName']
		print "namestring" + nameString
		room = Room.objects.filter(name=nameString)
		if room is None:
			print "no room"
			room = Room.objects.create(name=self.cleaned_data['name'], description=self.cleaned_data['description'], capacity=self.cleaned_data['capacity'], notes=self.cleaned_data['notes'], equipment=self.cleaned_data['equipment'])
		else:
			print "room found"
			room.name = self.cleaned_data['name']
			description = self.cleaned_data['description']
			capacity = self.cleaned_data['capacity']
			notes = self.cleaned_data['notes']
			equipment = self.cleaned_data['equipment']

		room.save()
		return room

class DeleteRoomForm(forms.Form):
	roomName = forms.CharField(widget=forms.HiddenInput(), initial='defaultRoom')
	def deleteRoom(self):
		nameString=self.cleaned_data['roomName']
		print("name: " + nameString)
		print("delete1")
		Room.objects.filter(name=nameString).delete()
		return HttpResponseRedirect('/')

# Course Form
class AddCourseForm(forms.Form):
   course_name = forms.CharField()
   descripton = forms.CharField()
   equipment_req = forms.CharField()

   def addCourse(self):
      course = Course(course_name = self.cleaned_date['course_name'],
                  descripton = self.cleaned_date['description'],
                  equipment_req = self.cleaned_data['equipment_req'])
      course.save(); 
