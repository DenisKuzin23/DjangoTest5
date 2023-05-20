from django import forms


class EditNewForm(forms.Form):
    topic = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
