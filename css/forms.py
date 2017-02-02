from django import forms

#  Invite Form
class InviteForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    UserType = forms.ChoiceField(
                choices = ((0, 'scheduler'), (1, 'faculty'))
                );
