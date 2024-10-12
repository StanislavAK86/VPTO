from django.db import models

# Create your models here.
#модель  для курса катигирии карточек

class CategoryCards(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.name
    
class Cards(models.Model):
    category = models.ForeignKey(CategoryCards, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='cards_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class VideoCurses(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='video_curses/')
    category = models.ForeignKey(CategoryCards, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name