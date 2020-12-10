from django.contrib import admin

from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import HierarchicalTag, TaggedContentItem, ContentItem
from mptt.admin import DraggableMPTTAdmin


# class TreeTagAdmin(TreeTag):
#     prepopulated_fields = ('slug': ('title',)),

admin.site.register(
    HierarchicalTag,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
    prepopulated_fields = {'slug': ('name',)}
)

admin.site.register(TaggedContentItem)
admin.site.register(ContentItem)