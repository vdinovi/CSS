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

