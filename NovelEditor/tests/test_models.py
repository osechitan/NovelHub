from django.test import TestCase
from django.contrib.auth import get_user_model
from .factory import UserFactory
from ..models import Novel, NovelHistory

User = get_user_model()

class TestNovelModel(TestCase):
    def setUp(self):
        """ユーザー/小説作成"""
        super().setUp()

        self.user = UserFactory()
        self.novel = self.user.novel_set.get()

    def test_novel_revert(self):
        # 小説に紐づく小説履歴を作成
        novel_history = NovelHistory.objects.create(
            novel_id = self.novel,
            title = self.novel.title,
            body = self.novel.body,
            revision_id = self.novel.revision_id,
        )

        # 小説更新
        self.novel.title = '更新タイトル'
        self.novel.body = '更新本文'
        self.novel.revision_id = 1
        self.novel.save()

        novel_history_v2 = NovelHistory.objects.create(
                novel_id=self.novel,
                title=self.novel.title,
                body=self.novel.body,
                revision_id=2
            )
        
        # 小説を戻す処理実行
        Novel().novel_revert(novel_history.id)

        # 小説が戻っていることを確認
        novel_reverted = Novel.objects.get(id=self.novel.id)
        self.assertEqual(novel_reverted.title, novel_history.title)
        self.assertEqual(novel_reverted.body, novel_history.body)
        self.assertEqual(novel_reverted.revision_id, 2)

        def test_novel_revert_validation_err(self):
            try:
                # 小説を戻す処理実行する際に、uuid形式でないものを渡す
                Novel().novel_revert('test')
            except Novel.DoesnotExist:
                # 404エラーが出ていればOK
                self.assertTrue(True)
            else:
                # 404エラーが出ない場合NG
                 self.assertTrue(False)


class TestNovelHistoryModel(TestCase):
    def setUp(self):
        """ユーザー/小説作成"""
        super().setUp()

        self.user = UserFactory()
        self.novel = self.user.novel_set.get()

    def test_create_history_data(self):
        # 小説履歴を作成する処理実行
        NovelHistory().create_history_data(
                novel=self.novel,
                title=self.novel.title,
                body=self.novel.body,
                revision_id=self.novel.revision_id
            )
        novel_history = NovelHistory.objects.get()
        self.assertEqual(novel_history.title, self.novel.title)
        self.assertEqual(novel_history.body, self.novel.body)
        self.assertEqual(novel_history.revision_id, self.novel.revision_id)