from django import forms


class SearchForm(forms.Form):
    author = forms.ChoiceField()
    topic = forms.CharField(required=False)
    date = forms.DateField(required=False, input_formats=['%d.%m.%Y'])
