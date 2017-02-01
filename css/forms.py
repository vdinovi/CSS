from django import forms

class InviteForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    UserType = forms.IntegerField()
