from django.db import models

class News(models.Model):
    id = models.AutoField(primary_key=True, db_column='news_ID')
    title = models.CharField(max_length=100)
    content = models.TextField()
    autor = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    

    class Meta:
        db_table = 'News'
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    def __str__(self):
        return self.title
    

""" 
добавление новостей
news = news.objects.create(title = 'ПРЕСЕЧЕНА ПОПЫТКА ВВОЗА В РОССИЙСКУЮ ФЕДЕРАЦИЮ НАРКОТИЧЕСКИХ СРЕДСТВ В ОСОБО КРУПНОМ РАЗМЕРЕ', content = 'Сотрудниками Пограничного управления ФСБ России по Республике Северная Осетия-Алания во взаимодействии с Северо-Осетинской таможней Северо-Кавказского таможенного управления ФТС России пресечена попытка ввоза в Российскую Федерацию наркотических средств в особо крупном размере. В пункте пропуска Верхний Ларс в оборудованном тайнике грузового транспортного средства обнаружено 2112 брикетов с наркотическим средством гашиш массой более 200 кг. Проводится проверка, по результатам которой будет принято процессуальное решение.', autor = 'ПС ФСБ', date = '2022-01-01')
 """

""" 
чтение новостей
news = news.objects.all()
news = news.objects.get(id = 1)
 """
""" 
for new in news.objects.all():
    print(new.content)
    """