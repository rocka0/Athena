from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50, label="Name")
    password = forms.CharField(max_length=10, label="Password")
    about = forms.CharField(max_length=500, label="About")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label="Userame")
    password = forms.CharField(max_length=10, label="Password")
