from django.urls import path
from .views import PostsList #index, detail, 

urlpatterns = [
    path('', PostsList.as_view()),
    #path('news_list/', index, name='index'),
    #path('new/<int:pk>', detail, name='detail'),
]