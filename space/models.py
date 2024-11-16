from django.db import models

# Create your models here.
class News(models.Model):
    banner = models.ImageField(upload_to='banners/')
    created_at = models.DateTimeField(auto_now_add=True)