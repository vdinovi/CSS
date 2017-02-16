from django import forms
from django.core.mail import send_mail
from css.models import CUser, Room
from django.http import HttpResponseRedirect

#Login Form
class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

#  Invite Form
class InviteUserForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()

    def send_invite(self, usertype):
        send_mail('Invite to register for CSS',
                   self.cleaned_data['name'] + ', you have been invited to register for CSS',
                   'registration@inviso-css',
                   [self.cleaned_data['email']])

# Registration Form
class RegisterUserForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    user_type = forms.ChoiceField(label='Usertype', choices=[('faculty', 'faculty'), ('scheduler', 'scheduler')])
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def save(self):
        user = CUser.create(email=self.cleaned_data['email'],
                            password=self.cleaned_data['password2'],
                            user_type=self.cleaned_data['user_type'])
        user.set_name(self.cleaned_data['first_name'], self.cleaned_data['last_name'])
        user.save()
        return user


# Delete Form
class DeleteUserForm(forms.Form):
    email = forms.CharField(label='Confirm email')

    # TODO: Delete user
    def delete_user(self):
        CUser.get_user(email=self.cleaned_data['email']).delete()

class AddRoomForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    capacity = forms.IntegerField()
    notes = forms.CharField()
    equipment = forms.CharField()

    def save(self):
		nameString = self.cleaned_data['name']
		resultRooms = Room.objects.filter(name=nameString)
		room = Room.objects.create(name=self.cleaned_data['name'], description=self.cleaned_data['description'], capacity=self.cleaned_data['capacity'], notes=self.cleaned_data['notes'], equipment=self.cleaned_data['equipment'])
		room.save()
		return room

class EditRoomForm(forms.Form):
	name = forms.CharField(widget=forms.HiddenInput(), initial='defaultRoom')
	description = forms.CharField()
	capacity = forms.IntegerField()
	notes = forms.CharField()
	equipment = forms.CharField()

	def save(self):
		nameString = self.cleaned_data['name']
		resultRooms = Room.objects.filter(name=nameString)
		room = resultRooms[0]
		room.name = self.cleaned_data['name']
		room.description = self.cleaned_data['description']
		room.capacity = self.cleaned_data['capacity']
		room.notes = self.cleaned_data['notes']
		room.equipment = self.cleaned_data['equipment']
		room.save()

class DeleteRoomForm(forms.Form):
	roomName = forms.CharField(widget=forms.HiddenInput(), initial='defaultRoom')
	def deleteRoom(self):
		nameString=self.cleaned_data['roomName']
		Room.objects.filter(name=nameString).delete()
		return

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