from django.db import models
import uuid
from django.utils import timezone

from accounts.models import CustomUser

class Novel(models.Model):
    """小説モデル"""
    class Meta:
        db_table = 'novel'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='タイトル', max_length=255)
    body = models.TextField(verbose_name='本文', null=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', null=True)

    def __str__(self):
        return self.title

    # 履歴モデルから戻す処理
    def novel_revert(self, history_id):
        novel_history = NovelHistory.objects.get(id=history_id)
        novel = Novel.objects.get(id=novel_history.novel_id.id)
        novel.title = novel_history.title
        novel.body = novel_history.body
        novel.updated_at = timezone.now()
        novel.save()
        return novel


class NovelHistory(models.Model):
    """小説変更履歴モデル"""
    class Meta:
        db_table = 'novel_history'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    novel_id = models.ForeignKey(Novel, verbose_name='小説ID', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='タイトル', max_length=255, null=True)
    body = models.TextField(verbose_name='本文', null=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)

    def __str__(self):
        return self.title

    # 小説に紐づく履歴データ作成
    def create_history_data(self, novel, title='title', body='内容'):
        novel_history = NovelHistory()
        novel_history.novel_id = novel
        novel_history.title = title
        novel_history.body = body
        novel_history.save()

        return novel_history


class NovelInfo(models.Model):
    """小説設定モデル"""
    class Meta:
        db_table = 'novel_info'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    novel_id = models.ForeignKey(Novel, verbose_name='小説ID', on_delete=models.CASCADE)
    outline = models.TextField(verbose_name='本文', null=True)
    hero = models.CharField(verbose_name='主人公名', max_length=255, null=True)
    heroine = models.CharField(verbose_name='ヒロイン', max_length=255, null=True)

    def __str__(self):
        return str(self.id)