from django import forms
from django.core.mail import EmailMessage


from .models import Novel
from .models import NovelHistory


class NovelCreateForm(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ('title', 'body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NovelUpdateForm(forms.ModelForm):
    class Meta:
        model = NovelHistory
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        print('formのprintarg={}'.format(args))
        print('formのprintkwargs={}'.format(kwargs))
        super().__init__(*args, **kwargs)