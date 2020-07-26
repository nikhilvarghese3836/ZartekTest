from django.conf.urls import url
from .views import PostViewSet,PostLikesViewSet
from rest_framework import renderers

posts_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
posts_like_list = PostLikesViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    url(r'^posts/', posts_list, name='posts'),
    url(r'^postlikes/', posts_like_list, name='postlikes'),
]
