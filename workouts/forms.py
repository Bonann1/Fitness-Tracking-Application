from django import forms
from .models import Workout, WorkoutExercise


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ('title', 'date', 'duration', 'notes')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ('exercise', 'sets', 'reps', 'weight', 'distance')

    def clean(self):
        cleaned_data = super().clean()
        sets = cleaned_data.get('sets')
        reps = cleaned_data.get('reps')
        distance = cleaned_data.get('distance')
        if not distance and not (sets and reps):
            raise forms.ValidationError(
                'Compila almeno serie + ripetizioni oppure la distanza.'
            )
        return cleaned_data
