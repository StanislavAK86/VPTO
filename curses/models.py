from django.db import models
import hashlib
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
    file_hash = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.file:
            self.file_hash = self.calculate_file_hash(self.file)
        super().save(*args, **kwargs)

    def calculate_file_hash(self, file):
        hash_md5 = hashlib.md5()
        for chunk in file.chunks():
            hash_md5.update(chunk)
        return hash_md5.hexdigest()