from django.db import models
import uuid

from accounts.models import CustomUser

class NovelPost(models.Model):
    class Meta:
        db_table = 'novel_post'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='タイトル', max_length=255)
    body = models.TextField(verbose_name='本文', null=True)
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
