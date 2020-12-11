"""test_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from userapp.views import signup, login
from tags.views import TagsUserList, TagViewSet, UserList, UserTagsList, UserTagsViewSet

snippet_list = TagViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy'
})

user_tags_list = UserTagsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    # tags
    path('api/tags/', snippet_list),
    path('api/tags/<str:tags>', TagsUserList.as_view()),

    # users
    path('api/user_list/', UserList.as_view()),
    path('api/user_tag/', UserTagsList.as_view()),
    path('api/user_tag/<int:pk>', user_tags_list),

    # admin
    path('admin/', admin.site.urls),

    # auth
    path('api-auth/', include('rest_framework.urls')),
    path('api/signup', signup),
    path('api/login', login),
]
