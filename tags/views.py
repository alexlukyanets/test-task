from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import permission_classes, api_view, action
from rest_framework.renderers import JSONRenderer
from .models import ContentItem, TaggedContentItem, HierarchicalTag
from userapp.permissions import MyPermission
from .serializers import ReadHierarchicalTagSerializer, TagsUserListSerializer, UserListSerializer, UserTagsSerializer
from functools import partial
from userapp.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class TagViewSet(viewsets.ViewSet):
    def list(self, request):
        if request.method == 'GET':
            get_queryset = HierarchicalTag.objects.root_node(tree_id=1).get_ancestors(include_self=True)
            serializer = ReadHierarchicalTagSerializer(get_queryset, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def create(self, request):

        if request.method == 'POST':

            try:
                key = self.request.data['tag']
                if not key:
                    return JsonResponse({"error": f"Check body data "}, safe=False,
                                        status=status.HTTP_400_BAD_REQUEST)
            except:
                return JsonResponse({"error": f"Check body data "}, safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)
            try:
                exist = TaggedContentItem.objects.filter(tag__name=key)
                if not exist:
                    post_instance = ContentItem.objects.create()
                    new = post_instance.tags.add(key)
                else:
                    return JsonResponse({"error": f"Tag already exist"}, safe=False,
                                        status=status.HTTP_400_BAD_REQUEST)

                return JsonResponse(data={"succesful": f'Tag {key} was created'}, safe=False,
                                    status=status.HTTP_201_CREATED)
            except:
                return JsonResponse({"error": f"Tag already exist"}, safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        try:
            name = self.request.data['name']
            id = self.request.data['id']
            new_name = self.request.data['new_name']
        except:
            return JsonResponse({"error": f"Check your body data"}, safe=False,
                                status=status.HTTP_400_BAD_REQUEST)
        if id and name and new_name and name != new_name:
            try:
                query = HierarchicalTag.objects.get(id=int(id),
                                                    name=name)
                try:
                    HierarchicalTag.objects.get(name=new_name)
                    return JsonResponse({"success": f"The new name='{new_name}' already exist"}, safe=False,
                                        status=status.HTTP_400_BAD_REQUEST)
                except:

                    query.name = new_name
                    query.save()
                    return JsonResponse({"success": f"Tag id='{id}', name='{name}' update to '{new_name}'"}, safe=False,
                                        status=status.HTTP_200_OK)

            except:
                return JsonResponse({"error": f"Tag {id} {name} doesn't exist"}, safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"error": f"Check your body data"}, safe=False,
                                status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        key = self.request.data["tag"]
        tags = TaggedContentItem.objects.filter(tag__name="Python")
        print(tags)
        if tags.exists():
            for tag in tags:
                tag.content_object.delete()
                tag.delete()
                tag.tag.delete()
                return JsonResponse({"success": f"Tag {key} was deleted"}, safe=False,
                                    status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": f"This tag {key} doesn't exist"}, safe=False,
                                status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'create' or 'update' or 'delete':
            permission_classes = [IsAdminUser, partial(MyPermission, ['POST', 'PUT', 'DELETE'])]
        return [permission() for permission in permission_classes]


class TagsUserList(generics.ListAPIView):
    serializer_class = TagsUserListSerializer
    permission_classes = [partial(MyPermission, ['GET'])]

    def get_queryset(self):
        keys = str(self.kwargs['tags']).split('+')
        user = []
        queryset = []
        for t in TaggedContentItem.objects.filter(tag__name__in=keys):
            if t.content_object.user not in user:
                user.append(t.content_object.user)
                queryset.append(t)
        return queryset


class UserList(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [partial(MyPermission, ['GET'])]
    queryset = User.objects.all()


class UserTagsList(generics.ListAPIView):
    serializer_class = UserTagsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserTagsViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk):
        if request.method == 'GET':
            get_queryset = User.objects.filter(pk=pk)
            if get_queryset:
                serializer = UserTagsSerializer(get_queryset, many=True)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": f"User doesn't exist"}, safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        if request.method == 'PUT':
            try:
                user = User.objects.get(pk=pk)
            except:
                return JsonResponse({"error": f"User doen't exist"}, safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)
            if user.id != self.request.user.id and not self.request.user.is_staff:
                return JsonResponse({"error": f"You aren't admin"}, safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                tags = str(self.request.data['tag']).split(' ')

                not_added_tags = ""
                for tag in tags:
                    exist = TaggedContentItem.objects.filter(content_object__user_id=user.id,
                                                             tag__name=tag)
                    if not exist:
                        post_instance = ContentItem.objects.create(user=user)
                        new = post_instance.tags.add(tag)
                    else:
                        not_added_tags += tag + " "

                if not_added_tags:
                    return JsonResponse({"success": f"Tags doesn't add {not_added_tags}becouse exist in {user}"},
                                        safe=False,
                                        status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"success": f"Update {str(tags)}"}, safe=False,
                                        status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        if request.method == 'DELETE':
            try:
                user = User.objects.get(pk=pk)
            except:
                return JsonResponse({"error": f"User doen't exist"}, safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)
            if user.id != self.request.user.id and not self.request.user.is_staff:
                return JsonResponse({"error": f"You aren't admin"}, safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                keys = str(self.request.data['tag']).split(' ')
                not_delteted_tags = ""
                for tag in keys:
                    tags = TaggedContentItem.objects.filter(tag__name=tag)
                    if tags.exists():
                        for tag in tags:
                            tag.content_object.delete()
                            tag.delete()
                            tag.tag.delete()
                    else:
                        not_delteted_tags += tag + " "

                if not_delteted_tags:
                    return JsonResponse({"success": f"Tags doesn't delete {not_delteted_tags}becouse doesn't exist in {user}"},
                                        safe=False,
                                        status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"success": f"Delete {str(keys)}"}, safe=False,
                                        status=status.HTTP_200_OK)


    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [partial(MyPermission, ['GET'])]
        elif self.action == 'update' or 'destroy':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
