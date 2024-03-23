from django.db import models

# Create your models here.
class Post(models.Model):
    username = models.CharField(max_length=10)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['username']