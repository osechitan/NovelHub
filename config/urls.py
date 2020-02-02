from django.contrib import admin
from django.urls import path, include

from django.contrib.staticfiles.urls import static
from . import settings, local_settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('NovelEditor.urls')),
    path('accounts/', include('allauth.urls'))
]
