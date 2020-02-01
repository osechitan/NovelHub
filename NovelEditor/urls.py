from django.urls import path
from . import views

app_name = 'NovelHub'

urlpatterns = [
    path('', views.TopView.as_view()),
    path('home/', views.HomeView.as_view(), name='home'),
]