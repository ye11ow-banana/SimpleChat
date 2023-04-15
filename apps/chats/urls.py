from django.urls import path

from . import views

urlpatterns = [
    path('thread/create/', views.thread_creation),
    path('thread/<int:pk>/destroy/', views.thread_destroy),
]
