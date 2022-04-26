from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50, label="Name")
    password = forms.CharField(max_length=10, label="Password")
    about = forms.CharField(max_length=500, label="About")
    profile_pic = forms.CharField(max_length=120, label="profile_pic")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label="Userame")
    password = forms.CharField(max_length=10, label="Password")
