from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Token

class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, UserAdmin)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'expires_at', 'is_active')
    search_fields = ('user__email',)
    list_filter = ('is_active', 'expires_at')
