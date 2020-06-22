from django.urls import path
from . import views

app_name = 'NovelEditor'

urlpatterns = [
    path('list/', views.NovelPostListView.as_view(), name='novelpost_list'),
]