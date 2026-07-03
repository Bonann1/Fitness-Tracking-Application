from django import forms
from .models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ('title', 'description', 'goal_type', 'metric', 'target_value', 'deadline', 'status')
        labels = {
            'title': 'Titolo',
            'description': 'Descrizione',
            'goal_type': 'Tipo obiettivo',
            'metric': 'Metrica',
            'target_value': 'Valore target',
            'deadline': 'Scadenza',
            'status': 'Stato',
        }
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        goal_type = cleaned_data.get('goal_type')
        metric = cleaned_data.get('metric')
        target_value = cleaned_data.get('target_value')
        if goal_type == 'metric':
            if not metric:
                self.add_error('metric', 'Seleziona una metrica per un obiettivo a metrica.')
            if target_value is None:
                self.add_error('target_value', 'Inserisci un valore target per un obiettivo a metrica.')
        return cleaned_data
