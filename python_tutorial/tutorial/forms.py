from django import forms


class PostForm(forms.Form):
    destination = forms.CharField(max_length=256)
