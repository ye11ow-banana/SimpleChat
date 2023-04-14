from django.conf import settings
from django.contrib import admin
from django.urls import path, include

api_urls = [
    path('chats/', include('chats.urls')),
]

urlpatterns = [
    path('api/v1/', include(api_urls)),
]

if settings.DEBUG:
    urlpatterns.append(path('admin/', admin.site.urls))
