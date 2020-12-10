from treebeard.mp_tree import MP_Node
from taggit.models import TagBase, ItemBase, TaggedItemBase
from taggit.managers import TaggableManager
from django.db import models


class HierarchicalTag(TagBase, MP_Node):
    node_order_by = ['name']

    # depth = models.PositiveIntegerField(default=1)
    # path = models.CharField(max_length=255)

    def get_or_create(self):
        print('True')


class TaggedContentItem(TaggedItemBase):
    content_object = models.ForeignKey('ContentItem', on_delete=models.CASCADE)
    tag = models.ForeignKey('HierarchicalTag', on_delete=models.CASCADE)

    def get_or_create(self):
        print('True')


class ContentItem(models.Model):
    tags = TaggableManager(through=TaggedContentItem, blank=True)

    def get_or_create(self):
        print('True')
