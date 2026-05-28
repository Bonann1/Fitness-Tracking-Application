from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CoachFeedback


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in ('standard', 'coach'):
            raise forms.ValidationError('Ruolo non valido.')
        return role


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('bio', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class CoachFeedbackForm(forms.ModelForm):
    class Meta:
        model = CoachFeedback
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Scrivi il tuo feedback...'}),
        }
