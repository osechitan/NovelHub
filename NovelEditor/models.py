from decimal import *

from django.db import models
import uuid
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser

REVISION_ID = 1

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
    revision_id = models.IntegerField(verbose_name='バージョン', null=True)

    def __str__(self):
        return self.title

    # 履歴モデルから戻す処理
    def novel_revert(self, history_id):
        try:
            novel_history = get_object_or_404(NovelHistory, id=history_id)
        except ValidationError as validerr:
            raise Http404
        else:
            novel = get_object_or_404(Novel, id=novel_history.novel_id.id)
            novel.title = novel_history.title
            novel.body = novel_history.body
            novel.updated_at = timezone.now()

            revision_id_added = novel_history.revision_id + REVISION_ID
            novel.revision_id = revision_id_added
            novel.save()

            # 戻した小説と同じバージョンの履歴モデル作成
            NovelHistory().create_history_data(
                    novel = novel,
                    title = novel.title,
                    body = novel_history.body,
                    revision_id = revision_id_added
                )
        
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
    revision_id = models.IntegerField(verbose_name='バージョン', null=True)

    def __str__(self):
        return self.title

    def novelid(self):
        return self.novel_id.id

    # 小説に紐づく履歴データ作成
    def create_history_data(self, novel, title, body, revision_id):
        novel_history = NovelHistory()
        novel_history.novel_id = novel
        novel_history.title = title
        novel_history.body = body
        novel_history.revision_id = revision_id
        novel_history.save()

        return novel_history