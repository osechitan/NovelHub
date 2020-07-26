import factory
from NovelPost import models
from accounts.models import CustomUser


class NovelPostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.NovelPost

    title='タイトル'
    body='本文'



class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username='testadmin'
    email='admin@examle.com'
    password='pass'
    novel_post = factory.RelatedFactory(NovelPostFactory, 'user')
