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
    version = models.IntegerField(verbose_name='バージョン', default=1)
