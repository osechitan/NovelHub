from django.urls import path
from . import views

app_name = 'NovelPost'

urlpatterns = [
    path('', views.TopView.as_view()),
]