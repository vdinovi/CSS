from django import forms

#  Invite Form
class InviteUserForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()

    # TODO: send a link to the registration page with 
    #   the provided name, email, and 'faculty' as the usertype
    def send_faculty_invite(self):
        pass

    # TODO: send a link to the registration page with 
    #   the provided name, email, and 'faculty' as the usertype
    def send_scheduler_invite(self):
        pass


#  Delete Form
class DeleteUserForm(forms.Form):
    id = forms.IntegerField()


