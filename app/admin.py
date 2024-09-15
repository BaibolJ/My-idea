from django.contrib import admin
from .serializers import *
from .models import *
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    ordering = ['email', 'name']  # Сортируем по полю email, так как у вас больше нет поля username
    list_display = ['email', 'name', 'phone_number', 'is_supplier', 'is_active', 'is_staff']  # Обновляем отображаемые поля
    list_filter = ['is_active', 'is_staff', 'is_supplier']  # Обновляем фильтры

    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'phone_number')}),
        ('Personal info', {'fields': ('is_supplier', '')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_supplier'),
        }),
    )

    filter_horizontal = ()  # Убираем поля, котор


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Variety)
admin.site.register(Order)
admin.site.register(Objects)

