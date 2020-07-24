from django.urls import path
from . import views

app_name = 'NovelPost'

urlpatterns = [
    path('list/', views.NovelPostListView.as_view(), name='post_list'),
]