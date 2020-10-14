from django.urls import path
from . import views

app_name = 'NovelHub'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('novel-list/', views.NovelListView.as_view(), name='novel_list'),
    path('novel-detail/<pk>/', views.NovelDetailView.as_view(), name='novel_detail'),
    path('novel-create/', views.NovelCreateView.as_view(), name='novel_create'),
    path('novel-update/<pk>/', views.NovelUpdateView.as_view(), name='novel_update'),
    path('novel-revert/<pk>/', views.NovelRevertView.as_view(), name='novel_revert'),
    path('novel-delete/<pk>/', views.NovelDeleteView.as_view(), name='novel_delete'),
]