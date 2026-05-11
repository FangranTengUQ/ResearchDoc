from django import forms
from .models import Summary


class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Summary title'}),
        }
