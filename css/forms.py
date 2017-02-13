from django import forms
from django.core.mail import send_mail
from css.models import CUser, Room

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
    email = forms.EmailField()
    user_type = forms.ChoiceField(label='Usertype', choices=[('faculty', 'faculty'), ('scheduler', 'scheduler')])
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def save(self):
        user = CUser.objects.create_cuser(email=self.cleaned_data['email'],
                                          password=self.cleaned_data['password2'],
                                          user_type=self.cleaned_data['user_type'])
        user.save()
        return user


# Delete Form
class DeleteUserForm(forms.Form):
    id = forms.IntegerField()

    # TODO: Delete user
    def delete_user(self):
        pass

class AddRoomForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    capacity = forms.IntegerField()
    notes = forms.CharField()
    equipment = forms.CharField()

    def save(self):
        room = Room.objects.create(name=self.cleaned_data['name'],
                                   description=self.cleaned_data['description'],
                                   capacity=self.cleaned_data['capacity'],
                                   notes=self.cleaned_data['notes'],
                                   equipment=self.cleaned_data['equipment'])
        room.save()
        return room

class DeleteRoomForm(forms.Form):
    id = forms.IntegerField()

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
