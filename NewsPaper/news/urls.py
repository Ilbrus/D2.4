from django.urls import path
from .views import PostsList, PostsSearch, PostDetail, PostCreateNews, PostEdit, PostDelete, create_post

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'), 
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('create/', create_post, name='post_nw_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_nw_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_nw_delete'),
    path('search/', PostsSearch.as_view(), name='post_search'),
]