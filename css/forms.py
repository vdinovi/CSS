from django import forms
from .models import Room

#  Invite Form
class InviteForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()

    # TODO: send a link to the registration page with
    #   the provided name, email, and 'faculty' as the usertype
    def send_invite(self):
        pass


#  Delete Form
class DeleteForm(forms.Form):
    id = forms.IntegerField()

class AddRoomForm(forms.Form):
    name = forms.CharField()
    description = forms.EmailField()
    capacity = forms.IntegerField()
    notes = forms.CharField()
    equipment = forms.CharField()

class DeleteRoomForm
    id = forms.IntegerField()
