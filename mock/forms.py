from django.forms import ModelForm, Textarea, TextInput, Select, CheckboxInput

from .models import Mock


class MockForm(ModelForm):
    class Meta(object):
        model = Mock
        fields = ('title', 'status', 'response_body', 'is_active')

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'aria-describedby': 'title_help',
            }),
            'status': Select(attrs={
                'class': 'form-control',
                'aria-describedby': 'status_help',
            }),
            'response_body': Textarea(attrs={
                'rows': 8,
                'class': 'form-control',
                'aria-describedby': 'body_help',
            }),
            'is_active': CheckboxInput(attrs={
                'class': 'form-control',
                'aria-describedby': 'active_help',
            }),
        }
