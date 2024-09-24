from django import forms



class NewsForm(forms.Form):
    title = forms.CharField(label='Заголовок', max_length=255)
    content = forms.CharField(label='Текст', widget=forms.Textarea)

class AuthorizationForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=255)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
