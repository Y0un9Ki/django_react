from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # 여기에 추가적인 필드를 정의할 수 있습니다.
    location = models.CharField(max_length=100, blank=True, null=True)