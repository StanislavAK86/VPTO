from django import forms
from .models import News, ImageGroup, Image




class NewsForm(forms.ModelForm):

    title = forms.CharField(label='Заголовок', max_length=255, widget = forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(label='Текст', widget = forms.Textarea(attrs={'class':'form-control'}))

    
    
    class Meta:
        model = News
        fields = [ 'title', 'content']

#Добавим форму для создания группы галерий и загрузки фотокартинок 

class editImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['group', 'image', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }


class ImageGroupForm(forms.ModelForm):
    
    class Meta:
        model = ImageGroup
        fields = ['name']
        labels = {
            'name': 'Название',
        }

        


class AuthorizationForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=255)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
