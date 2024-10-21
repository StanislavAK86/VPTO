from django.db import models

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Название теста'
        verbose_name_plural = 'Названия тестов'

    def __str__(self):
        return self.name
class UserInfo(models.Model):
    full_name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'
    



class Question(models.Model):
    text = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Варианты ответа'
        verbose_name_plural = 'Варианты ответов'

    def __str__(self):
        return self.text

class Answer(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return str(self.user_info)
        