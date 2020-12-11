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


def parse_bytes(request, multy=False):
    d = str(request).split("&")
    if len(d) == 2 and multy == True:
        return False, False, False

    if len(d) == 3:
        id = d[0][2:].split("=")
        name = d[1].split("=")
        new_name = d[2][:-1].split("=")
        if id[0] == "id" and name[0] == 'name' and new_name[0] == 'new_name':
            return id[1], name[1], new_name[1]
        else:
            return False, False, False
    else:
        tag = d[0][2:].split("=")
        user = d[1][:-1].split("=")
        if tag[0] == "tag" and user[0] == 'user' or tag[0] == "id" and user[0] == 'name':
            return tag[1], user[1]
        else:
            return False, False


class TagViewSet(viewsets.ViewSet):
    def list(self, request):
        if request.method == 'GET':
            get_queryset = HierarchicalTag.objects.root_node(tree_id=1).get_ancestors(include_self=True)
            serializer = ReadHierarchicalTagSerializer(get_queryset, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def create(self, request):
        if request.method == 'POST':

            try:
                key = str(request.body)[7:-1]
                if not key:
                    return JsonResponse({"error": f"Check body data "}, safe=False,
                                        status=status.HTTP_400_BAD_REQUEST)
            except:
                return JsonResponse({"error": f"Check body data "}, safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)
            try:
                tag = HierarchicalTag.objects.create(name=key)
                return JsonResponse(data={"succesful": f'Tag {key} was created'}, safe=False,
                                    status=status.HTTP_201_CREATED)
            except:
                return JsonResponse({"error": f"Tag already exist"}, safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        id, name, new_name = parse_bytes(request.body, multy=True)
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
        keys = str(request.body)[7:-1].split('%20')
        tags = TaggedContentItem.objects.filter(tag__name__in=keys)
        if tags.exists():
            for tag in tags:
                tag.content_object.delete()
                tag.delete()
                tag.tag.delete()
                return JsonResponse({"success": f"Tag {keys} was deleted"}, safe=False,
                                    status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": f"This tag {keys} doesn't exist"}, safe=False,
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


def create(self, request):
    if request.method == 'POST':
        try:
            tag, user = parse_bytes(request.body)
        except:
            return JsonResponse({"error": f"Check body data "}, safe=False,
                                status=status.HTTP_400_BAD_REQUEST)
        if tag and user:
            user = User.objects.get(username=user)
            try:
                TaggedContentItem.objects.get(content_object__user_id=user.id,
                                              tag__name=tag)
                return JsonResponse({"error": f"Tag {tag} alredy exists"}, safe=False,
                                    status=status.HTTP_400_BAD_REQUEST)

            except:
                post_instance = ContentItem.objects.create(user=user)
                tags = post_instance.tags.add(tag)
                return JsonResponse(data={str(user): tag}, safe=False, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({"error": f"Check body data "}, safe=False,
                                status=status.HTTP_400_BAD_REQUEST)


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
            # try:
            user = User.objects.get(pk=pk)
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
                    return JsonResponse({"success": f"Tags doesn't add {not_added_tags}becouse exist in {user}"}, safe=False,
                                        status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"success": f"Update {str(tags)}"}, safe=False,
                                        status=status.HTTP_200_OK)
            # except:
            #     return JsonResponse({"error": f"User doesn't exist"}, safe=False,
            #                         status=status.HTTP_400_BAD_REQUEST)


    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [partial(MyPermission, ['GET'])]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
