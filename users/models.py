from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    photo = models.ImageField(upload_to='users/images/%Y/%m/%d', null=True, blank=True, verbose_name='Аватар')
    date_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='castom_users_set',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='castom_users_set',
        blank=True,
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.pk:  # If the instance already exists
            old_instance = User.objects.get(pk=self.pk)
            if old_instance.photo and self.photo != old_instance.photo:
                # Delete the old photo if it exists and is different from the new one
                old_instance.photo.delete(save=False)
        super().save(*args, **kwargs)
