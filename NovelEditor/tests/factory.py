import factory
from NovelEditor import models
from accounts.models import CustomUser


class NovelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Novel

    title='タイトル'
    body='本文'
    revision_id=1


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username='testadmin'
    email='admin@examle.com'
    password='pass'
    novel = factory.RelatedFactory(NovelFactory, 'user')