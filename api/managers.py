from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model where the email address is the unique identifier
    and has an is_admin field to allow access to the admin app 
    """
    def create_user(self, username, password, location, **extra_fields):
        # if not username:
        #     raise ValueError(_("이름을 넣어주세요"))
        # if not password:
        #     raise ValueError(_("패스워드를 넣어주세요"))
        # if not location:
        #     raise ValueError(_('사는 곳의 구를 적어주세요(서울한정)'))

        user = self.model(
            username=username,
            location=location,
            **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, location, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 1)

        if extra_fields.get('role') != 1:
            raise ValueError('Superuser must have role of Global Admin')
        return self.create_user(username, password, location, **extra_fields)