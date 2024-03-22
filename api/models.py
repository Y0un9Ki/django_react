from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # 여기에 추가적인 필드를 정의할 수 있습니다.
    location = models.CharField(max_length=100, blank=True, null=True)
    
    # 다음에 시간되면 class User(models.Model): 로 커스텀 유저로 만들어보기 -> username과 password, location 필드 추가해보기