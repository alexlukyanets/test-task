from rest_framework import serializers
from .models import ContentItem, HierarchicalTag, TaggedContentItem
from rest_framework_recursive.fields import RecursiveField
from userapp.models import User

class ReadHierarchicalTagSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    children = serializers.ListField(child=RecursiveField(), source='get_children', read_only=True)

    class Meta:
        model = HierarchicalTag
        fields = ['id', 'name', 'children', 'user']

    def get_user(self, model):
        if TaggedContentItem.objects.filter(tag_id=model.id).exists():
            return [o.content_object.user.username for o in TaggedContentItem.objects.filter(tag_id=model.id)]


class TagsUserListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='content_object.user.username')
    skills = serializers.SerializerMethodField()

    class Meta:
        model = TaggedContentItem
        fields = ['user', 'skills']

    def get_skills(self, model):
        return u", ".join(o.tag.name for o in
                          TaggedContentItem.objects.filter(content_object_id__user_id=model.content_object.user.id))


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined', 'is_company_admin', 'is_superuser']
