from django.urls import path

from . import views

urlpatterns = [
    path('thread/', views.thread_creation),
]
