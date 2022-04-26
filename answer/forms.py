from django import forms


class addAnswerForm(forms.Form):
    text = forms.CharField(max_length=1000, label="Text")


class addAnswerCommentForm(forms.Form):
    text = forms.CharField(max_length=500, label="Text")
