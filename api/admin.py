from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


# Register your models here.

User = get_user_model()

# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
    # fieldsets = [
    #     (None, {'fields': ('username', 'password')}),
    #     ('개인정보', {'fields': ('email',)}),
    #     ('추가필드', {'fields': ('location',)}),
    #     (
    #         '권한',
    #         {
    #             'fields': (
    #                 'is_active',
    #                 'is_staff',
    #                 'is_superuser',
    #             )
    #         }
    #     )
    # ]
    
admin.site.register(User)