from django import forms

class AddUser(forms.Form):
    username = forms.CharField(max_length=50,label="Name")
    password = forms.CharField(max_length=10,label="Password")
    about = forms.CharField(max_length=500,label="About")
    role = forms.BooleanField(required=False)