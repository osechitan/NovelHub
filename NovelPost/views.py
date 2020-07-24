from django.shortcuts import render
from django.views import generic, View
import logging

from .models import NovelPost

logger = logging.getLogger(__name__)

class NovelPostListView(generic.ListView):
    """
    投稿小説一覧表示用ビュー
    """

    model = NovelPost
    template_name = 'post_list.html'
    context_object_name = 'post_list'
