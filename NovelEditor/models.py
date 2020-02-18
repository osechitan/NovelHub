from accounts.models import CustomUser
from django.db import models
import uuid


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


class NovelInfo(models.Model):
    """小説設定モデル"""
    class Meta:
        db_table = 'novel_info'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    novel_id = models.ForeignKey(Novel, verbose_name='小説ID', on_delete=models.CASCADE)
    outline = models.TextField(verbose_name='本文', null=True)
    hero = models.CharField(verbose_name='主人公名', max_length=255, null=True)
    heroine = models.CharField(verbose_name='ヒロイン', max_length=255, null=True)
