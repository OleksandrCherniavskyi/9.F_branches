# forms.py
from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(max_length=250, label='Name')

    def clean_name(self):
        name = self.cleaned_data['name']
        # Capitalize the first letter of each word
        return ' '.join(word.capitalize() for word in name.split())