from django import forms
from django.core.mail import send_mail

#  Invite Form
class InviteUserForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()

    def send_invite(self, usertype):
        send_mail('Invite to register for CSS',
                   self.cleaned_data['name'] + ', you have been invited to register for CSS',
                   'registration@inviso-css',
                   [self.cleaned_data['email']])


# Delete Form
class DeleteUserForm(forms.Form):
    id = forms.IntegerField()

    # TODO: Delete user
    def delete_user(self):
        pass

# Course Form
class AddCourseForm(forms.Form):
   course_name = forms.CharField()
   descripton = forms.CharField(); 
   equipment_req = forms.CharField(); 

   def addCourse(self):
      course = Course(course_name = self.cleaned_date['course_name'],
                  descripton = self.cleaned_date['descripton'],
                  equipment_req = self.cleaned_data['equipment_req']); 
      course.save(); 

