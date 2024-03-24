from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.
# class User(AbstractUser):
#     # 여기에 추가적인 필드를 정의할 수 있습니다.
#     location = models.CharField(max_length=100, blank=True, null=True)
    
    # 다음에 시간되면 class User(models.Model): 로 커스텀 유저로 만들어보기 -> username과 password, location 필드 추가해보기
class UserManager(BaseUserManager):
    def create_user(self, username, location, password=None):
        user = self.model(
            username = username,
            location = location,
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, location, password=None):
        user = self.create_user(
            username=username,
            location=location
        )
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    # id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10, blank=False, unique=True)
    # password = models.CharField(max_length=20, blank=False, help_text='비밀번호를 8자리 이상으로 적어주세요')
    location = models.CharField(max_length=100, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
    
    def __str__(self):
        return self.username
    
