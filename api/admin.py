from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


# Register your models here.

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    fieldsets = [
        (None, {'fields': ('username', 'password')}),
        ('개인정보필드', {'fields': ('first_name', 'last_name', 'email')}),
        ('추가필드', {'fields': ('location',)}),
        (
            '권한',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_admin',
                )
            }
        )
    ]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
admin.site.register(User, CustomUserAdmin)