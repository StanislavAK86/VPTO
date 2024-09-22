from django import forms



class NewsForm(forms.Form):
    title = forms.CharField(label='Заголовок', max_length=255)
    content = forms.CharField(label='Текст', widget=forms.Textarea)
