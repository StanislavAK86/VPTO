from django.db import models

class News(models.Model):
    id = models.AutoField(primary_key=True, db_column='news_ID')
    title = models.CharField(max_length=100)
    content = models.TextField()
    autor = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        db_table = 'News'
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    def __str__(self):
        return self.title



class ImageGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Image(models.Model):
    group = models.ForeignKey(ImageGroup, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.description



