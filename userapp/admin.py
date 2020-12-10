from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from tags.models import ContentItem,TaggedContentItem, HierarchicalTag


class ContentItemTagInline(admin.TabularInline):
    model = ContentItem


class UserAdminCustom(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

    save_on_top = True
    inlines = [
        ContentItemTagInline,
    ]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Разрешения', {
            'fields': ('is_company_admin', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),

        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'is_company_admin', 'email', 'first_name', 'last_name', 'is_staff','tag_list')
    list_filter = ('contentitem__tags', 'is_staff', 'is_superuser', 'is_active', 'groups')


    # def get_queryset(self, request):
    #     return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.tag.name for o in TaggedContentItem.objects.filter(content_object_id__user_id=obj.id))


admin.site.register(User, UserAdminCustom)
