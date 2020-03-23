from django import forms

from .models import Novel
from .models import NovelHistory


class NovelCreateForm(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ('title', 'body', 'revision_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['revision_id'].initial = 1
        self.fields['revision_id'].widget.attrs['readonly'] = True
