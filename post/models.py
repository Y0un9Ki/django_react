from django.db import models
from api.models import User

# Create your models here.
class Post(models.Model):
    username = models.ForeignKey(User, blank=True, null=True, on_delete = models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['username']