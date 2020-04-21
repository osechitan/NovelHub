from django.test import TestCase
from ..forms import NovelCreateForm

class TestNovelCreateForm(TestCase):
    """CreateFormテスト"""

    def test_form_success(self):
        data = {
            'title': 'タイトル',
            'body': '本文',
            'revision_id': 1
        }
        form = NovelCreateForm(data)
        self.assertTrue(form.is_valid())
    
    def test_form_fail(self):
        # 空のデータを渡してバリデーションエラーを発生させる
        data = {}
        form = NovelCreateForm(data)
        self.assertFalse(form.is_valid())