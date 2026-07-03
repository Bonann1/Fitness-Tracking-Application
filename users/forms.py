from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CoachFeedback


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, label='Ruolo')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')
        labels = {'username': 'Nome utente'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Conferma password'

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in ('standard', 'coach'):
            raise forms.ValidationError('Ruolo non valido.')
        return role


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('bio', 'avatar')
        labels = {
            'bio': 'Biografia',
            'avatar': 'Avatar',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class CoachFeedbackForm(forms.ModelForm):
    class Meta:
        model = CoachFeedback
        fields = ('message',)
        labels = {'message': 'Messaggio'}
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Scrivi il tuo feedback...'}),
        }
