from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from .factory import UserFactory
from ..models import Novel, NovelHistory
from .. import views

User = get_user_model()

class TestNovelListView(TestCase):
    """ListViewのテスト"""

    def setUp(self):
        """ユーザー/小説作成"""
        super().setUp()

        self.user = UserFactory()
        self.novel = self.user.novel_set.get()
        self.request_factory = RequestFactory()
    
    def test_get_queryset(self):
        request = self.request_factory.get(reverse('NovelHub:novel_list'))
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user)
        self.assertContains(response, 'タイトル')
        self.assertContains(response, '本文')

    def test_redirect_unauthenticated_user(self):
        request = self.request_factory.get(reverse('NovelHub:novel_list'))
        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelListView.as_view()(request)
        
        # 認証されたユーザーでないため、リダイレクトされることを確認
        self.assertEqual(response.status_code, 302)


class TestNovelDetailView(TestCase):
    """DetailViewのテスト"""

    def setUp(self):
        """ユーザー/小説作成"""
        super().setUp()

        self.user = UserFactory()
        self.novel = self.user.novel_set.get()
        self.request_factory = RequestFactory()

    def test_get_detail(self):
        
        request = self.request_factory.get(reverse('NovelHub:novel_detail', kwargs={'pk': self.novel.id}))
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelDetailView.as_view()(request, pk=self.novel.id)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user)
        self.assertContains(response, self.novel.title)
        self.assertContains(response, self.novel.body)

    def test_redirect_unauthenticated_user(self):
        request = self.request_factory.get(reverse('NovelHub:novel_detail', kwargs={'pk': self.novel.id}))
        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelDetailView.as_view()(request, pk=self.novel.id)

        # 認証されたユーザーでないため、リダイレクトされることを確認
        self.assertEqual(response.status_code, 302)


class TestNovelCreateView(TestCase):
    """CreateViewのテスト"""

    def setUp(self):
        """ユーザー/小説作成"""
        super().setUp()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='pass'
        )

        self.request_factory = RequestFactory()

    def test_get(self):
        request = self.request_factory.get(reverse('NovelHub:novel_create'))
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = views.NovelCreateView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user)

    def test_post_null(self):
        data = {}
        request = self.request_factory.post(reverse('NovelHub:novel_create'), data=data)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_post_with_data(self):
        data = {
            'title': 'タイトル',
            'body': '本文',
            'revision_id': 1
        }
        request = self.request_factory.post(reverse('NovelHub:novel_create'), data=data)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)

        # 小説が作成されているかのテスト
        novel = Novel.objects.get(title='タイトル')
        self.assertEqual(novel.title, 'タイトル')
        self.assertEqual(novel.body, '本文')
        self.assertEqual(Novel.objects.count(), 1)

        # 小説に紐づく小説履歴が作成されているかのテスト
        novel_history = NovelHistory.objects.get(novel_id=novel)
        self.assertEqual(novel_history.title, novel.title)
        self.assertEqual(novel_history.body, novel.body)
        self.assertEqual(novel_history.revision_id, novel.revision_id)
        self.assertEqual(Novel.objects.count(), 1)

    def test_redirect_unauthenticated_user(self):
        data = {
            'title': 'タイトル',
            'body': '本文',
            'revision_id': 1
        }
        request = self.request_factory.post(reverse('NovelHub:novel_create'), data=data)
        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelCreateView.as_view()(request)

        # 認証されたユーザーでないため、リダイレクトされ、小説が作成されないことを確認
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Novel.objects.count(), 0)

class TestNovelUpdateView(TestCase):
    """UpdateViewのテスト"""
    def setUp(self):
        """ユーザー/小説作成"""
        super().setUp()
        self.user = UserFactory()
        self.novel = self.user.novel_set.get()
        self.request_factory = RequestFactory()

    def test_get(self):
        # 小説に紐づく小説履歴作成
        NovelHistory.objects.create(
                novel_id=self.novel,
                title=self.novel.title,
                body=self.novel.body,
                revision_id=1
            )

        request = self.request_factory.get(reverse('NovelHub:novel_update', kwargs={'pk': self.novel.pk}))
        request.user = self.user
        
        response = views.NovelUpdateView.as_view()(request, pk=self.novel.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user)

        # 小説履歴が取得されているか確認
        history_title = ''
        history_body = ''
        for h in response.context_data['history']:
            history_title = h.title
            history_body = h.body

        self.assertIsInstance(response.context_data, dict)
        self.assertEqual(history_title, self.novel.title)
        self.assertEqual(history_body, self.novel.body)

    def test_post_null(self):
        data = {}
        request = self.request_factory.post(reverse('NovelHub:novel_update', kwargs={'pk': self.novel.pk}), data=data)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelUpdateView.as_view()(request, pk=self.novel.id)
        self.assertEqual(response.status_code, 200)

    def test_post_with_data(self):
        data = {
            'title': '更新タイトル',
            'body': '更新本文',
            'revision_id': 1
        }

        request = self.request_factory.post(reverse('NovelHub:novel_update', kwargs={'pk': self.novel.pk}), data=data)
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelUpdateView.as_view()(request, pk=self.novel.id, data=data)
        self.assertEqual(response.status_code, 302)

        # 小説が更新されているかのテスト
        novel_updated = Novel.objects.get(id=self.novel.id)
        self.assertEqual(novel_updated.title, '更新タイトル')
        self.assertEqual(novel_updated.body, '更新本文')
        self.assertEqual(novel_updated.revision_id, 2)

        # 小説に紐づく小説履歴が更新されているかのテスト
        novel_history = NovelHistory.objects.get(novel_id=novel_updated.id)
        self.assertEqual(novel_history.title, novel_updated.title)
        self.assertEqual(novel_history.body, novel_updated.body)
        self.assertEqual(novel_history.revision_id, novel_updated.revision_id)

    def test_redirect_unauthenticated_user(self):
        data = {
            'title': '更新タイトル',
            'body': '更新本文',
            'revision_id': 1
        }
        request = self.request_factory.post(reverse('NovelHub:novel_update', kwargs={'pk': self.novel.pk}), data=data)
        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelUpdateView.as_view()(request, pk=self.novel.id, data=data)
        
        # 認証されたユーザーでないため、リダイレクトされ、小説が更新されないことを確認
        self.assertEqual(response.status_code, 302)
        novel_updated = Novel.objects.get(id=self.novel.id)
        self.assertEqual(novel_updated.title, 'タイトル')
        self.assertEqual(novel_updated.body, '本文')
        self.assertEqual(novel_updated.revision_id, 1)

class TestNovelRevertView(TestCase):
    """RevertViewのテスト"""
    def setUp(self):
        """ユーザー/小説作成"""
        super().setUp()
        self.user = UserFactory()
        self.novel = self.user.novel_set.get()
        self.request_factory = RequestFactory()
        # 小説に紐づく小説履歴を作成
        self.novel_history = NovelHistory.objects.create(
            novel_id = self.novel,
            title = self.novel.title,
            body = self.novel.body,
            revision_id = self.novel.revision_id,
        )
  
    def test_post(self):
        # 小説更新
        self.novel.title = '更新タイトル'
        self.novel.body = '更新本文'
        self.novel.revision_id = 1
        self.novel.save()

        # 小説更新後小説履歴モデルも作成
        novel_history_v2 = NovelHistory.objects.create(
                novel_id=self.novel,
                title=self.novel.title,
                body=self.novel.body,
                revision_id=2
            )

        request = self.request_factory.post(reverse('NovelHub:novel_revert', kwargs={'pk': self.novel_history.id}))
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelRevertView.as_view()(request, pk=self.novel_history.id)
        self.assertEqual(response.status_code, 302)

        novel_reverted = Novel.objects.get(id=self.novel.id)
        self.assertEqual(novel_reverted.title, self.novel_history.title)
        self.assertEqual(novel_reverted.body, self.novel_history.body)
        self.assertEqual(novel_reverted.revision_id, 2)

    def test_redirect_unauthenticated_user(self):
        self.novel.title = '更新タイトル'
        self.novel.body = '更新本文'
        self.novel.revision_id = 1
        self.novel.save()

        # 小説更新後小説履歴モデルも作成
        novel_history_v2 = NovelHistory.objects.create(
                novel_id=self.novel,
                title=self.novel.title,
                body=self.novel.body,
                revision_id=2
            )
        
        request = self.request_factory.post(reverse('NovelHub:novel_revert', kwargs={'pk': self.novel_history.id}))
        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelRevertView.as_view()(request, pk=self.novel_history.id)
        
        # 認証されたユーザーでないため、リダイレクトされ、小説が更新されないことを確認
        self.assertEqual(response.status_code, 302)
        novel_updated = Novel.objects.get(id=self.novel.id)
        self.assertEqual(novel_updated.title, '更新タイトル')
        self.assertEqual(novel_updated.body, '更新本文')
        self.assertEqual(novel_updated.revision_id, 1)


class TestNovelDeleteView(TestCase):
    """DeleteViewのテスト"""
    def setUp(self):
        """ユーザー/小説作成"""
        super().setUp()
        self.user = UserFactory()
        self.novel = self.user.novel_set.get()
        self.request_factory = RequestFactory()

    def test_get(self):
        request = self.request_factory.get(reverse('NovelHub:novel_delete', kwargs={'pk': self.novel.id}))
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelDeleteView.as_view()(request, pk=self.novel.id)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        request = self.request_factory.post(reverse('NovelHub:novel_delete', kwargs={'pk': self.novel.id}))
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
    
        response = views.NovelDeleteView.as_view()(request, pk=self.novel.id)
        self.assertEqual(response.status_code, 302)

        # 小説が削除されていることの確認
        self.assertEqual(Novel.objects.count(), 0)

    def test_redirect_unauthenticated_user(self):
        request = self.request_factory.post(reverse('NovelHub:novel_delete', kwargs={'pk': self.novel.id}))
        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = views.NovelDeleteView.as_view()(request, pk=self.novel.id)
        
        # 認証されたユーザーでないため、リダイレクトされ、小説が削除されないことを確認
        self.assertEqual(response.status_code, 302)
        novel_updated = Novel.objects.get(id=self.novel.id)
        self.assertEqual(novel_updated.title, 'タイトル')
        self.assertEqual(novel_updated.body, '本文')
        self.assertEqual(novel_updated.revision_id, 1)
        self.assertEqual(Novel.objects.count(), 1)