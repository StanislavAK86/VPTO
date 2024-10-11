from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


class CustomAuthenticationForm(AuthenticationForm):

    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class':'form-control'}),
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
    )

class RegistrationForm(forms.ModelForm):


    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
    )

    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'password', 'password2' )
        label = {
            'username': 'Имя пользователя',
            'email': 'Почта',
            'first_name': 'Имя',
           
        }
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
        }

    def clean_password2(self):
        pas = self.cleaned_data
        
        if pas['password']  != pas['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return pas['password2']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже существует')
        return email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user