from django import forms
from .models import News



class NewsForm(forms.ModelForm):

    title = forms.CharField(label='Заголовок', max_length=255, widget = forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(label='Текст', widget = forms.Textarea(attrs={'class':'form-control'}))
    autor = forms.CharField(label='Автор', max_length=255, widget = forms.TextInput(attrs={'class':'form-control'}))
    
    
    class Meta:
        model = News
        fields = [ 'title', 'content', 'autor']

    # id = forms.IntegerField(label='ID', widget=forms.HiddenInput)
    # title = forms.CharField(label='Заголовок', max_length=255)
    # content = forms.CharField(label='Текст', widget=forms.Textarea)
    # autor = forms.CharField(label='Автор', max_length=255)
    # date = forms.DateField(label='Дата', auto_now_add=True)


class AuthorizationForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=255)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
