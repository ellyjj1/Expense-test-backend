from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# 你可以自定义用户管理界面
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

# 注册用户模型
admin.site.unregister(User)  # 先注销默认的用户管理
admin.site.register(User, UserAdmin)  # 注册自定义的用户管理
