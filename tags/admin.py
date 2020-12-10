from django.contrib import admin

from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import HierarchicalTag, ContentItem, TaggedContentItem


class MyAdmin(TreeAdmin):
    form = movenodeform_factory(HierarchicalTag)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(HierarchicalTag, MyAdmin)
admin.site.register(ContentItem)
admin.site.register(TaggedContentItem)
