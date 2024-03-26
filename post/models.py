from django.db import models
from api.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

class Post(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete = models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # comment = models.TextField(blank=True, null=True)    
    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return self.comment