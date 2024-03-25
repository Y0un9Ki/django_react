from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, username, location, password=None):
        user = self.model(
            username = username,
            location = location,
        )
        user.set_password(password)
        user.save()
        return user

    # 관리자 user 생성
    def create_superuser(self,username, location, password=None):
        user = self.create_user(
            username=username,
            location=location
        )
        user.set_password(password)
        user.is_admin = True
        user.save()
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=5, null=False, blank=False, unique=True)
    location = models.CharField(max_length=10, null=False, blank=False)
    
    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    
    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 nickname으로 설정
    USERNAME_FIELD = 'username'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['location','password']

    def __str__(self):
        return self.username