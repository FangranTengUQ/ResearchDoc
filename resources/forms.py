from django import forms
from .models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'resource_type', 'file', 'url', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resource title'}),
            'resource_type': forms.Select(attrs={'class': 'form-select', 'id': 'id_resource_type'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        resource_type = cleaned_data.get('resource_type')
        file = cleaned_data.get('file')
        url = cleaned_data.get('url')

        if resource_type == 'file':
            if not file:
                self.add_error('file', 'Please upload a PDF file.')
            elif file:
                if not file.name.lower().endswith('.pdf'):
                    self.add_error('file', 'Only PDF files are allowed.')
                if file.size > 10 * 1024 * 1024:
                    self.add_error('file', 'File size must be under 10MB.')
        elif resource_type == 'url':
            if not url:
                self.add_error('url', 'Please enter a URL.')

        return cleaned_data
