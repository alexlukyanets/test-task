from __future__ import unicode_literals
from functools import partial
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from taggit.managers import TaggableManager
from taggit.models import TagBase, ItemBase, GenericTaggedItemBase
from userapp.models import User


class HierarchicalTag(MPTTModel, TagBase):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('rubric', kwargs={'pk': self.pk})

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name


class TaggedContentItem(ItemBase):
    content_object = models.ForeignKey('ContentItem', on_delete=models.CASCADE)
    tag = models.ForeignKey('HierarchicalTag', related_name='tags', on_delete=models.CASCADE)


class ContentItem(models.Model):
    tags = TaggableManager(through=TaggedContentItem, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    #
    # def __str__(self):
    #     return str(self.tags.names().get())
