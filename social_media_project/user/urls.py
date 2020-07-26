from django.conf.urls import url
from .views import UserViewSet,ReactViewSet,PostLikesViewSet,ListUserViewSet


users_create = UserViewSet.as_view({
    'post': 'create'
})

users_list = ListUserViewSet.as_view({
    'get': 'list',
})

react_list = ReactViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
posts_like_list = PostLikesViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    url(r'^users/', users_create, name='userss'),
    url(r'^getusers/', users_list, name='users'),
    url(r'^react/', react_list, name='react'),
    url(r'^likedetails/', posts_like_list, name='react'),

]