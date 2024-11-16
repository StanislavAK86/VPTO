from django import forms
from .models import  CategoryCards, Cards, VideoCurses


# форма для добавление видео по модели VideoCurses

class VideoCursesForm(forms.ModelForm):
    class Meta:
        model = VideoCurses
        fields = ['name', 'file', 'category']
        labels = {
            'name': 'Название видео',
            'file': 'Файл видео',
            'category': 'Категория видео',
        }
    