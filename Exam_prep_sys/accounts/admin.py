from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_instructor', 'is_learner', 'is_staff')
    list_filter = ('is_instructor', 'is_learner', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_instructor', 'is_learner', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_instructor', 'is_learner'),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

# Customizing the Django admin site titles
admin.site.site_header = "Exam preparation System Admin Portal"
admin.site.site_title = "MCQ Admin Panel"
admin.site.index_title = "Welcome to the Admin Dashboard"