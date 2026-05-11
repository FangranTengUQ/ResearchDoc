from django import forms
from .models import ComparisonTable


class ComparisonTableForm(forms.ModelForm):
    class Meta:
        model = ComparisonTable
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Table title'}),
        }
