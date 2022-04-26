from django import forms


class addQuestionForm(forms.Form):
    title = forms.CharField(max_length=500, label="Title")
    text = forms.CharField(max_length=1000, label="Text")


class addQuestionCommentForm(forms.Form):
    text = forms.CharField(max_length=500, label="Text")
