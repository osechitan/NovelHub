# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from NovelEditor.models import Novel

from NovelEditor.models import Novel
from NovelEditor.tests.factory import UserFactory

User = get_user_model()

class TestNovelListView(TestCase):
    """ListViewのテスト"""

    def setUp(self):
        """ユーザー/小説作成"""
        super().setUp()

        self.user = UserFactory()
        self.client = Client()
        self.client.force_login(self.user)
    
    def test_get_queryset(self):
        response = self.client.get('/novel-list/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user)
        self.assertTemplateUsed(response, 'novel_list.html')
        self.assertContains(response, 'タイトル')
        self.assertContains(response, '本文')

    def test_redirect_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get('/novel-list/')

        self.assertEqual(response.status_code, 302)


class TestNovelDetailView(TestCase):
    """DetailViewのテスト"""

    def setUp(self):
        """ユーザー/小説作成"""
        super().setUp()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='pass'
        )
        self.novel = Novel.objects.create(
            user=self.user,
            title='タイトル',
            body='本文'
        )
        self.user = UserFactory()
        self.client = Client()
        self.client.force_login(self.user)

    def test_get_detail(self):
        response = self.client.get(reverse('NovelHub:novel_detail', kwargs={'pk': self.novel.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'novel_detail.html')
        self.assertContains(response, self.user)
        self.assertEqual(response.context['object'].title, 'タイトル')
        self.assertEqual(response.context['object'].body, '本文')


    def test_redirect_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('NovelHub:novel_detail', kwargs={'pk': self.novel.pk}))

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
        self.novel = Novel.objects.create(
            user=self.user,
            title='タイトル',
            body='本文'
        )
        self.client = Client()
        self.client.force_login(self.user)