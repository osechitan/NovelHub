from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from .factory import UserFactory
from ..models import NovelPost
from .. import views

User = get_user_model()

class TestPostNovelListView(TestCase):
    """ListViewのテスト"""

    def setUp(self):
        """ユーザー/投稿小説作成"""
        super().setUp()

        self.user = UserFactory()
        self.novel = self.user.novelpost_set.get()
        self.request_factory = RequestFactory()

    def test_get_queryset(self):
        request = self.request_factory.get(reverse('NovelPost:post_list'))
        request.user = self.user
        setattr(request, 'session', 'session')

        response = views.NovelPostListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'タイトル')
        self.assertContains(response, '本文')
