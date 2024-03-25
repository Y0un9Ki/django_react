from django.db import models
from api.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete = models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # comment = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['user']