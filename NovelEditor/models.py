from accounts.models import CustomUser
from django.db import models


class Novel(models.Model):
    """小説モデル"""
    class Meta:
        db_table = 'novel'

    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='タイトル', max_length=255)
    body = models.TextField(verbose_name='本文', null=True)
    created_at = models.DateTimeField(verbose_name='作成日')
    updated_at = models.DateTimeField(verbose_name='更新日', null=True)

