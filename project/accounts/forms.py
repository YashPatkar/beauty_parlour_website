"""
Accounts app - Custom forms for registration etc.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    """Registration with username, password1, password2, and optional email."""
    email = forms.EmailField(
        required=False,
        label='Email (optional)',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com',
            'autocomplete': 'email',
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username',
            'autocomplete': 'username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password',
        })
        if 'email' in self.fields and 'placeholder' not in (self.fields['email'].widget.attrs or {}):
            self.fields['email'].widget.attrs.setdefault('placeholder', 'your@email.com')

    def save(self, commit=True):
        user = super().save(commit=commit)
        if self.cleaned_data.get('email'):
            user.email = self.cleaned_data['email'].strip()
            if commit:
                user.save()
        return user
