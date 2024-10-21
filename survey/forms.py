from django import forms
from .models import UserInfo, Answer, Question, Choice, Group

class UserInfoForm(forms.ModelForm):
    #group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
    class Meta:
        model = UserInfo
        fields = ['full_name', 'institution', 'team']
        labels = {
            'full_name': 'Ф.И.О.',
            'institution': 'Название учебного заведения',
            'team': 'Команда, которую представляете',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['chosen_choice']

class QuestionForm(forms.ModelForm):
    new_group = forms.CharField(max_length=255, required=False, label="Новая группа")
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, label="Выберите группу")
    class Meta:
        model = Question
        fields = ['text', 'group', 'is_published', 'new_group']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.all()

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Текст ответа', 'required': True}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_correct'].widget.attrs.update({'class': 'form-check-input'})