from django.urls import path
from . import views
from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    # path('<int:year>/<int:month>/<int:day>/<slug:post>/',
    #      views.post_detail,
    #      name='post_detail'),
    path('article/<slug:slug>', views.post_detail, name='post_detail'),
    # 这里的参数类型不要写slug，否则又会忽视中文，写str就行了
    path('tag/<str:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostFeed(), name='post_feed'),
]
