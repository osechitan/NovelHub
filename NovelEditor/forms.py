from django import forms
from django.core.mail import EmailMessage

from .models import Novel


class NovelCreateForm(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ('title', 'content', 'photo1', 'photo2', 'photo3', )
