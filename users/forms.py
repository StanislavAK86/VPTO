import datetime
from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model



class CustomAuthenticationForm(AuthenticationForm):

    username = forms.CharField(
        label='Логин',
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
            'username': 'Логин',
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
    
class ProfileUserform(forms.ModelForm):
    this_year = datetime.date.today().year


    date_birth = forms.DateField(
        label='Дата рождения',
        widget=forms.SelectDateWidget(
            years=range(this_year - 100, this_year - 6)
        ),
        required=False
    )
    photo = forms.ImageField(
        label='Аватар',
        required=False
    )
    username = forms.CharField(
        disabled=False,
        label='Логин',
        widget=forms.TextInput(attrs={'class':'form-control'}),
        required=False
    )
    first_name = forms.CharField(
        disabled=False,
        label='Имя',
        widget=forms.TextInput(attrs={'class':'form-control'}),
        required=False
    )
    email = forms.EmailField(
        disabled=False,
        label='Почта',
        widget=forms.EmailInput(attrs={'class':'form-control'}),
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'email', 'date_birth', 'photo')
        label = {
            'username': 'Логин',
            'first_name': 'Имя',
            'email': 'Почта',
            'date_birth': 'Дата рождения',
            'poto': 'Аватар',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
        }
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Старый пароль'}),
    )
    new_password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Новый пароль'}),
    )

    new_password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Новый пароль'}),
    )



