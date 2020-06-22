from django.shortcuts import render
from django.views import generic, View

from .models import NovelPost

class NovelPostListView(generic.ListView):
    """
    投稿小説一覧表示用ビュー
    """

    model = NovelPost
    template_name = 'post_list.html'

    def get_queryset(self):
        """
        投稿された小説一覧を返す関数
        """

        novel_posts = NovelPost.objects.all().order_by('-created_at').reverse()
        return novel_posts