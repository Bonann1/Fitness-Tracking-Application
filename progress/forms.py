from django import forms
from django.utils import timezone
from .models import ProgressEntry
from goals.models import Goal


class ProgressEntryForm(forms.ModelForm):
    class Meta:
        model = ProgressEntry
        fields = ('date', 'value', 'goal', 'notes')
        labels = {
            'date': 'Data',
            'value': 'Valore',
            'goal': 'Obiettivo',
            'notes': 'Note',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['goal'].queryset = Goal.objects.filter(user=user)
        self.fields['goal'].required = False

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > timezone.now().date():
            raise forms.ValidationError('La data non può essere nel futuro.')
        return date
