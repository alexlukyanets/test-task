from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdminCustom(UserAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

    save_on_top = True
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Теги', {'fields': ('tags',)}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Разрешения', {
            'fields': ('is_active', 'is_company_admin', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_company_admin', 'is_staff', 'tag_list')
    list_filter = ('tags', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('tags', 'username', 'first_name', 'last_name', 'email')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        try:
            return u", ".join(o.name for o in obj.tags.all())
        except:
            return "-"


admin.site.register(User, UserAdminCustom)
