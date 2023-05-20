from django import forms


class CreateNewForm(forms.Form):
    author = forms.ChoiceField()
    topic = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
